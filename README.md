# Source

## 0. Set up
- Install MongoDB & MySQL

## 1. Scrape data
Script: [load_data.py](src/load_data.py)
### Workflow
- Send `request` to `Tiki` web API to get product information
- Set rule to `sleep` after 50 or 100 requests to avoid blocking `IP`
- Add `APIs` failed to send request to a set for later handling
- Insert scraped data directly to the `product` collection within the `tiki` MongoDB database
- output: [sample_output (MongoDB)](data/processed_data/sample_output (MongoDB).json)

## 2. 
