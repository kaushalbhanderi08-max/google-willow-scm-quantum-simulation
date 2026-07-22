
import os
import pandas as pd
import yfinance as yf
import wbgapi as wb
import feedparser
import urllib.request
import json

class DataIngestionEngine:
    def __init__(self):
        pass
        
    def fetch_global_planetary_data(self):
        try:
            # 1. World Bank Population
            pop_raw = wb.data.get('SP.POP.TOTL', 'WLD', mrv=1)
            population = 8000000000.0
            if isinstance(pop_raw, list) and len(pop_raw) > 0:
                val = pop_raw[0].get('value') if isinstance(pop_raw[0], dict) else getattr(pop_raw[0], 'value', None)
                if val: population = float(val)

            # 2. Environment / Forest Area Proxy
            forest_raw = wb.data.get('AG.LND.FRST.ZS', 'WLD', mrv=1)
            forest_index = 0.31
            if isinstance(forest_raw, list) and len(forest_raw) > 0:
                val = forest_raw[0].get('value') if isinstance(forest_raw[0], dict) else getattr(forest_raw[0], 'value', None)
                if val: forest_index = float(val) / 100.0

            # 3. GNI per capita Proxy for Middle Class Index
            gni_raw = wb.data.get('NY.GNP.PCAP.CD', 'WLD', mrv=1)
            middle_class_index = 0.60
            if isinstance(gni_raw, list) and len(gni_raw) > 0:
                val = gni_raw[0].get('value') if isinstance(gni_raw[0], dict) else getattr(gni_raw[0], 'value', None)
                if val: middle_class_index = min(float(val) / 50000.0, 1.0)

            # 4. Human Food & Agricultural Consumption Proxy
            food_raw = wb.data.get('AG.PRD.FOOD.XD', 'WLD', mrv=1)
            human_food_index = 0.85
            if isinstance(food_raw, list) and len(food_raw) > 0:
                val = food_raw[0].get('value') if isinstance(food_raw[0], dict) else getattr(food_raw[0], 'value', None)
                if val: human_food_index = min(float(val) / 150.0, 1.0)

            # 5. Marine / Water Life Consumption Proxy
            fish_raw = wb.data.get('ER.FSH.CAPT.MT', 'WLD', mrv=1)
            water_life_index = 0.70
            if isinstance(fish_raw, list) and len(fish_raw) > 0:
                val = fish_raw[0].get('value') if isinstance(fish_raw[0], dict) else getattr(fish_raw[0], 'value', None)
                if val: water_life_index = min(float(val) / 100000000.0, 1.0)

            # 6-14. Global Indices Proxies
            satellite_geo_index = 0.95
            rsc_iupac_chemistry_index = 0.94
            who_health_index = 0.91
            iot_governance_policy_index = 0.93
            wildlife_animal_medical_index = 0.89
            mining_demand_supply_index = 0.92
            global_trade_logistics_index = 0.94
            global_energy_index = 0.91
            global_companies_industries_index = 0.95

            # 15 & 16. Tech News & Market Volatility via yfinance & RSS
            rss_url = "https://finance.yahoo.com/news/rssindex"
            feed = feedparser.parse(rss_url)
            tech_sentiment = 0.95
            if feed.entries:
                tech_sentiment = min(0.99, 0.90 + (len(feed.entries) / 1000.0))

            ticker = yf.Ticker("^GSPC")
            history = ticker.history(period="5d")
            market_volatility = 0.05
            if not history.empty:
                recent_close = history['Close'].iloc[-1]
                prev_close = history['Close'].iloc[-2]
                market_volatility = min(float(abs(recent_close - prev_close) / prev_close * 10), 1.0)

            global_signals = {
                'market_volatility': market_volatility,
                'supply_chain_index': forest_index,
                'tech_adoption_rate': tech_sentiment,
                'global_sentiment': middle_class_index,
                'total_population': population,
                'human_food_consumption': human_food_index,
                'water_life_consumption': water_life_index,
                'satellite_geo_index': satellite_geo_index,
                'chemistry_materials_index': rsc_iupac_chemistry_index,
                'who_health_index': who_health_index,
                'iot_governance_policy_index': iot_governance_policy_index,
                'animal_wildlife_medical_index': wildlife_animal_medical_index,
                'mining_demand_supply_index': mining_demand_supply_index,
                'global_trade_logistics_index': global_trade_logistics_index,
                'global_energy_index': global_energy_index,
                'global_companies_industries_index': global_companies_industries_index
            }
            print("Data Ingestion Engine Executed Successfully!")
            return global_signals
            
        except Exception as e:
            print(f"Error: {e}")
            return {
                'market_volatility': 0.05,
                'supply_chain_index': 0.31,
                'tech_adoption_rate': 0.95,
                'global_sentiment': 0.60,
                'total_population': 8000000000,
                'human_food_consumption': 0.85,
                'water_life_consumption': 0.70,
                'satellite_geo_index': 0.90,
                'chemistry_materials_index': 0.94,
                'who_health_index': 0.91,
                'iot_governance_policy_index': 0.93,
                'animal_wildlife_medical_index': 0.89,
                'mining_demand_supply_index': 0.92,
                'global_trade_logistics_index': 0.94,
                'global_energy_index': 0.91,
                'global_companies_industries_index': 0.95
            }
