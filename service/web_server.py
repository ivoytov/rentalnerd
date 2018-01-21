import web
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

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
    return render.good_sell(property_id)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()