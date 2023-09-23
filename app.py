from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/mehulbatra/Desktop/Programming/Python Addy/Flask/Hooman-Website/static/imgs'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///admin.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class myStock(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    product = db.Column(db.String(200),nullable = False)
    mrp = db.Column(db.String(200),nullable = False)
    actual_price = db.Column(db.String(200),nullable = False)
    product_category = db.Column(db.String(200),nullable = False)
    file_name = db.Column(db.String(200),nullable = False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# db.cre    ate_all()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/", methods=["POST", "GET"])
def home():

    return render_template("index.html")


@app.route("/about", methods=["POST", "GET"])
def about():

    return render_template("Aboutus.html")


@app.route("/collection/dogfood", methods=["POST", "GET"])
def dogfood():

    all_products =  myStock.query.all()

    return render_template("Dog_Food.html",all_products=all_products)

@app.route("/collection/large_collar", methods=["POST", "GET"])
def largecollar():

    all_products =  myStock.query.all()

    return render_template("Large_Collar.html",all_products=all_products)

@app.route("/collection/small_collar", methods=["POST", "GET"])
def smallcollar():

    all_products =  myStock.query.all()

    return render_template("Small_Collar.html",all_products=all_products)


@app.route("/checkout", methods=["POST", "GET"])
def checkout():

    return render_template("checkout.html")



@app.route('/admin', methods =['GET', 'POST'])
def update():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_mrp = request.form['productMRP']
        product_actual_price = request.form['product_actual_price']
        productCategory = request.form['productCategory']
        file = request.files['file']
        image_name = file.filename
        final_upload = myStock(product = product_name,mrp=product_mrp,actual_price = product_actual_price,product_category = productCategory,file_name = image_name)

        db.session.add(final_upload)
        db.session.commit()
        
        if 'file' not in request.files:
            return redirect(request.url)


        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return redirect(url_for('uploaded_file', filename=file.filename))
    
        # return render_template('admin.html')

    all_products =  myStock.query.all()
    return render_template('admin.html',all_products=all_products)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('update'))

@app.route('/delete/<int:sno>/')
def delete(sno):
    stock = myStock.query.filter_by(sno=sno).first()
    db.session.delete(stock)
    db.session.commit()
    return redirect('/admin')

    



if __name__ == "__main__":
    app.run(debug=True,port=5001)
