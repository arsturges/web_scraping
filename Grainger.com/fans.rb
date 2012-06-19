require 'nokogiri'
require 'open-uri'
require 'csv'

@prices = Array.new
@serial_numbers = Array.new
@descriptions = Array.new
@urls = Array.new
@categories = Array.new
@subcategories = Array.new
@subsubcategories = Array.new

urls = CSV.read("fan_urls.csv")
(0..urls.length - 1).each do |index|
  puts urls[index][0]
  doc = Nokogiri::HTML(open(urls[index][0]))
  
  #the last bread crumb does not have an anchor tag, which allows the following logic
  bread_crumbs_length = doc.css('div[style="padding-left:10px;"] a').length + 1
  puts "bread crumbs length: #{bread_crumbs_length}"
  if bread_crumbs_length == 2
    category = doc.css('a + font')[0].content
    sub_category = "na" 
    sub_sub_category = "na" 
  elsif bread_crumbs_length == 3
    category = doc.css('div[style="padding-left:10px;"] a:first-child + a')[0].content
    sub_category = doc.css('a + font')[0].content
    sub_sub_category = "na" 
  elsif bread_crumbs_length == 4
    category = doc.css('div[style="padding-left:10px;"] a:first-child + a')[0].content
    sub_category = doc.css('div[style="padding-left:10px;"] a:first-child + a + a')[0].content
    sub_sub_category = doc.css('a + font')[0].content
  else
    category = "na"
    sub_category = "na"
    sub_sub_category = "na"
  end

  doc.css('div > b > font').each do |price|
    @prices << price.content
    @urls << urls[index][0]
    @categories << category
    @subcategories << sub_category
    @subsubcategories << sub_sub_category
  end

  doc.css('div#contentalt1 table[align] div:first-child b').each do |serial_number|
	  @serial_numbers << serial_number.content
  end

  doc.css('table + table tr + tr td a').each do |description|
    @descriptions << description.content unless description.content.length < 2
  end
end
 
CSV.open("fans.csv", "wb") do |row|
  row << ["category", "sub-category", "sub-sub-category", "serial number", "price", "description", "url"]
  (0..@prices.length - 1).each do |index|
    row << [
      @categories[index], 
      @subcategories[index], 
      @subsubcategories[index], 
      @serial_numbers[index], 
      @prices[index], 
      @descriptions[index], 
      @urls[index]]
  end
end
