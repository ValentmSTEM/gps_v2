from tornado import Server
import TemplateAPI



def dummy():
    print "Started"


def indexPage(response):
    response.write(TemplateAPI.render('website.html', response, {}))


server = Server('0.0.0.0', 80)
server.register("/", indexPage)
server.run(dummy)
