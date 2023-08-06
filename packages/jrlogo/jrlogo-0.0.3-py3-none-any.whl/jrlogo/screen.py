import turtle

from . import color

_screen = None

def instance() -> turtle._Screen:
    global _screen
    if _screen is not None:
        return _screen
    _screen = turtle.Screen()
    # _screen.tracer(0, 0)    # 默认关闭动画
    _screen.listen()        # 默认开启监听
    return _screen

def setup(width : int = 800, height : int = 600):
    instance().setup(width, height)
    
def title(title : str = "jrlogo"):
    instance().title(title)
    
def bgcolor(c : color.Color = None):
    if c is None:
        return instance().bgcolor()
    c = color.colorstr(c)
    return instance().bgcolor(c)
    
def bgpic(filename : str):
    if filename is None:
        return instance().bgpic()
    return instance().bgpic(filename)

def done():
    instance().mainloop()

def bye():
    instance().bye()
    
if __name__=="__main__":
    setup()
    bgcolor(color.yellowgreen)
    done()