import csv
from flask import Flask, render_template, request, send_file, redirect
from scrapper import search_apartment

app = Flask(__name__)

db = {}

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")

    if not keyword or keyword.strip() == "":
        return redirect("/")
    
    # 💡 깔끔하게 변경된 부동산 전용 함수 호출
    apt_results = search_apartment(keyword)
    db[keyword] = apt_results
        
    return render_template(
        "search.html", 
        matzips=enumerate(apt_results), 
        keyword=keyword, 
        count=len(apt_results)
    )

@app.route("/download")
def download():
    keyword = request.args.get("keyword")

    if not keyword or keyword.strip() == "":
        return redirect("/")
    
    if keyword in db:
        apt_data = db[keyword]
    else:
        apt_data = search_apartment(keyword)
        db[keyword] = apt_data
        
    filename = "./daegu-apt-data.csv"
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["번호", "아파트 단지명(동)", "공급/전용 면적", "소재지", "매물 호가"])
        
        for idx, item in enumerate(apt_data):
            writer.writerow([
                idx + 1, 
                item["name"], 
                item["category"], 
                item["address"], 
                item.get("price", "N/A")
            ])
            
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)