import web

urls = (
  '/', 'index',
  '/good_sell', 'good_sell'
)

render = web.template.render('templates/')

class index:
  def GET(self):
    return render.index()

class good_sell:
  def GET(self):
    return render.good_sell()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()