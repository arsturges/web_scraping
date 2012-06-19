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
@diameters = Array.new
@max_cfms = Array.new

urls = CSV.read("fan_urls.csv")
(0..urls.length - 1).each do |index|
  puts urls[index][0]
  doc = Nokogiri::HTML(open(urls[index][0]))
  
  #the last bread crumb does not have an anchor tag, which allows the following logic
  bread_crumbs_length = doc.css('div[style="padding-left:10px;"] a').length + 1
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
    if description.content.length > 2 #eliminate blanks picked up by Nokogiri CSS selectors
      @descriptions << description.content 
      match_inches_regex = /\d+(\s+in|")/ # "42 in"
      match_digits_regex = /\d+/ # "42"
      if description.content[match_inches_regex] #some descriptions don't include diameter
        @diameters << description.content[match_inches_regex][match_digits_regex].to_i # 42
      else
        @diameters << "na"
      end

      grab_cfm_string_regex = /\(\d{2,}.+CFM\)|(\d+,?\d*\sCFM)/
      remove_extras_regex = /\(|\)|\s?CFM|,/ #remove parenthesis, " CFM", and comma
      split_string_regex = /\s?\/\s?|\s?-\s?|\s?to\s?|\s?or\s?/ #split based on slash, hyphen, "to", "or"
      if description.content[grab_cfm_string_regex]
        cfm_string = description.content[grab_cfm_string_regex]
        cfm_string_without_extra_characters = cfm_string.gsub(remove_extras_regex,"")
        array_of_cfms = cfm_string_without_extra_characters.split(split_string_regex)
        @max_cfms << array_of_cfms.max 
      else
        @max_cfms << "na"
      end
    end
  end
end
 
CSV.open("fans.csv", "wb") do |row|
  row << ["category", "sub-category", "sub-sub-category", "serial number", "price", "description", "diameter", "max cfm", "url"]
  (0..@prices.length - 1).each do |index|
    row << [
      @categories[index], 
      @subcategories[index], 
      @subsubcategories[index], 
      @serial_numbers[index], 
      @prices[index], 
      @descriptions[index], 
      @diameters[index],
      @max_cfms[index],
      @urls[index]]
  end
end
