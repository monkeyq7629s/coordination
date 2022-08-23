# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 16:32:04 2022
@author: LEE HSIN-CHI
"""
#初始化flask伺服器
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

#處理路由
@app.route("/")
def index():
    return render_template("index.html")

import requests
from bs4 import BeautifulSoup
#單點查詢路由
@app.route("/search_single")
def search_single():
    longtitude = request.args.get("longtitude", "")
    latitude = request.args.get("latitude", "")
    url = "https://api.nlsc.gov.tw/other/TownVillagePointQuery/"
    response = requests.get(url + longtitude + "/" + latitude + "/4326")
    soup = BeautifulSoup(response.text, "xml")
    cityName = str(soup.find("ctyName"))
    cityName = cityName[9:]
    cityName = cityName[:-10]
    townName = str(soup.find("townName"))
    townName = townName[10:]
    townName = townName[:-12]
    return render_template("search.html", text=cityName+townName)

import pandas as pd
#多點查詢路由
@app.route("/search_multiple")
def search_multiple():
    Input = request.args.get("Input", "")
    data = pd.read_excel(Input, usecols = ["編號", "經度", "緯度"], dtype={"編號":str, "經度":str, "緯度":str})
    url = "https://api.nlsc.gov.tw/other/TownVillagePointQuery/"
    result = pd.DataFrame(columns = ["查詢結果"])
    for i in range(data.shape[0]):
        response = requests.get(url + data['經度'][i] + '/' + data['緯度'][i] + "/4326")
        soup = BeautifulSoup(response.text, "xml")
        cityName = str(soup.find("ctyName"))
        cityName = cityName[9:]
        cityName = cityName[:-10]
        townName = str(soup.find("townName"))
        townName = townName[10:]
        townName = townName[:-12]
        temp = cityName+townName
        result = result.append({"查詢結果":temp},ignore_index=True)
      
    return render_template("search.html", text=result)

if __name__ == "__main__":
    app.run(port = 5000)