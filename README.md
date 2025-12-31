# 📁 ASSET — Image Research & Reference Collector


**Asset** is an image research tool made for **creators, designers, marketers, and content researchers** to quickly gather visual references during brainstorming or content development. 

It pulls image results via **SerpAPI**, caches them for later access, and opens a **keyboard-controlled image viewer** where you can browse, filter visually, and selectively save only what you want — making research fast, organized, and clutter-free.


---

## 🚀 What Asset Helps You Do


- Search and collect visual references for any topic


- Cache search results so repeated research costs *zero API calls*


- Browse images one-by-one using a clean Tkinter viewer


- Save only the useful images — no bulk dump mess


- Automatically sorts saved images into folders by keyword


- Perfect for content ideation, illustration moodboards, article creative, web/social media assets, etc.


---

## ⌨ Controls Inside Viewer


		- `SPACE` → Next Image  
		
		- `ENTER` → Save Image to folder  
		
		- `ESC` → Exit Viewer  


---

## 🛠 Installation & Setup


### 1. Clone the project  
		
		```bash
		git clone https://github.com/yourusername/asset.git
		cd asset
		```  


### 2. Install requirements  
		
		```bash
		pip install -r requirements.txt
		```  


### 3. Add API Key  
Create a `.env` file:  
		
		```
		SERP_API_KEY=YOUR_KEY_HERE
		```  


Get a key → https://serpapi.com/  


---

## ▶️ How to Use Asset


Run the tool:  
		
		```bash
		python asset.py
		```  


Enter keywords for the images you want to research:  
		
		```
		=== ASSET — IMAGE RESEARCH TOOL ===
		Enter first keyword: futuristic architecture
		Enter second keyword: editorial book design
		```  


## A viewer opens. Browse visually. Save only what inspires you.  


Saved output organizes itself like:  
		
		```
		futuristic_architecture_images/
				001_google_com.jpg
				002_pinterest_com.jpg
		
		
		editorial_book_design_images/
				001_behance_net.jpg
				002_dribbble_com.jpg
		```  


