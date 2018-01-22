import web
import os 
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(dir_path + '/' + '../scraper/Scripts/'))
import good_sell_service

# Overriding the model_path
setattr(good_sell_service, 'model_path', dir_path + '/models/')

urls = (
  '/', 'index',
  '/good_sell', 'good_sell'
)

print dir_path
render = web.template.render( dir_path + '/templates/' )

class index:
  def GET(self):
    return render.index()

class good_sell:
  def GET(self):
    params = web.input(property_id=False)
    print params
    property_id = params.property_id
    
    if property_id != False:
      predictions = good_sell_service.good_sell_service(property_id)  
      return predictions

    else:
      return "Example usage: http://localhost:8080/good_sell?property_id=9024040"
      # return render.good_sell(property_id, predictions)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()