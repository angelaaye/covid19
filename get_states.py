import scrapy

class UnemploymentInsurance(scrapy.Spider):
    name = "UI"

    start_urls = ['https://oui.doleta.gov/unemploy/claims.asp']
    
    def parse(self, response):
        states = response.xpath('//*[@id="states"]/option/text()').getall()
        abbrevs = response.xpath('//*[@id="states"]/option/@value').getall()
        with open("states.txt", "w") as f:
            for s, a in zip(states, abbrevs):
                f.write(f"{s} {a}\n")