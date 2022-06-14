from app import views


def setup_routes(app):
    app.router.add_get("/", views.index)
    app.router.add_get("/stop", views.stop)
    app.router.add_get("/start", views.start)
    app.router.add_get("/restart", views.restart)
    app.router.add_get("/toggle_control", views.toggle_control) 
