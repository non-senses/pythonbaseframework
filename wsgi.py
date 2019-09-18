from app import create_app
app = create_app('dm-pricing-baseprice-msrp')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
