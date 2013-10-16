
class Plugin(object):
    """docstring for Plugin

    plugin is a base class
    it has all interfaces that will be called
    instances of this class ususally get added to a plugins list
    this list will have its members called with all methods invoked.

    Creating an ATB Bar in __init__ is required in the class that is based on this class
    Show at least some info about the Ref_Detector
    self._bar = atb.Bar(name = self.__class__.__name__, label='your_label',
                help="ref detection parameters", color=(50, 50, 50), alpha=100,
                text='light', position=atb_pos,refresh=.3, size=(300, 150))
    """
    def __init__(self):
        self._alive = True

    @property
    def alive(self):
        """This field indicates of the instance should be detroyed
        Writing False to this will schedule the instance for deletion
        """
        if not self._alive:
            if hasattr(self,"cleanup"):
                try:
                    self.cleanup()
                except:
                    print "cleanup failed. This is a bug. Please report"

        return self._alive

    @alive.setter
    def alive(self, value):
        if isinstance(value,bool):
            self._alive = value

    def on_click(self,pos):
        """
        gets called when the user clicks in the window screen
        """
        pass

    def update(self,img,recent_pupil_posotions):
        """
        gets called once every frame
        """
        pass

    def gl_display(self):
        """
        gets called once every frame
        """
        pass

    def cleanup(self):
        """gets called when the plugin get terminated.
        This happends either volunatily or forced.
        if you have an atb bar or glfw window destroy it here.
        """
        pass

    def __del__(self):
        self._alive = False


'''
# example of a plugin with atb bar and its own private window + gl-context:

from glfw import *
from plugin import Plugin

# window calbacks
def on_resize(window,w, h):
    active_window = glfwGetCurrentContext()
    glfwMakeContextCurrent(window)
    adjust_gl_view(w,h)
    glfwMakeContextCurrent(active_window)

class Example_Plugin(Plugin):

    def __init__(self,g_pool,atb_pos=(0,0)):
        Plugin.__init__(self)

        self.window_should_open = False
        self.window_should_close = False
        self._window = None
        self.fullscreen = c_bool(0)
        self.monitor_idx = c_int(0)
        self.monitor_handles = glfwGetMonitors()
        self.monitor_names = [glfwGetMonitorName(m) for m in self.monitor_handles]
        monitor_enum = atb.enum("Monitor",dict(((key,val) for val,key in enumerate(self.monitor_names))))
        #primary_monitor = glfwGetPrimaryMonitor()

        atb_label = "example plugin"
        # Creating an ATB Bar.
        self._bar = atb.Bar(name =self.__class__.__name__, label=atb_label,
            help="ref detection parameters", color=(50, 50, 50), alpha=100,
            text='light', position=atb_pos,refresh=.3, size=(300, 100))
        self._bar.add_var("monitor",self.monitor_idx, vtype=monitor_enum)
        self._bar.add_var("fullscreen", self.fullscreen)
        self._bar.add_button("  show window   ", self.do_open, key='c')

    def do_open(self):
        if not self._window:
            self.window_should_open = True

    def open_window(self):
        if not self._window:
            if self.fullscreen.value:
                monitor = self.monitor_handles[self.monitor_idx.value]
                mode = glfwGetVideoMode(monitor)
                height,width= mode[0],mode[1]
            else:
                monitor = None
                height,width= 640,360

            self._window = glfwCreateWindow(height, width, "Plugin Window", monitor=monitor, share=None)
            if not self.fullscreen.value:
                glfwSetWindowPos(self._window,200,0)

            on_resize(self._window,height,width)

            #Register callbacks
            glfwSetWindowSizeCallback(self._window,on_resize)
            glfwSetKeyCallback(self._window,self.on_key)
            glfwSetWindowCloseCallback(self._window,self.on_close)

            # gl_state settings
            active_window = glfwGetCurrentContext()
            glfwMakeContextCurrent(self._window)
            gl.glEnable(gl.GL_POINT_SMOOTH)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            gl.glEnable(gl.GL_BLEND)
            gl.glClearColor(1.,1.,1.,0.)
            glfwMakeContextCurrent(active_window)

            self.window_should_open = False


    def on_key(self,window, key, scancode, action, mods):
        if not atb.TwEventKeyboardGLFW(key,int(action == GLFW_PRESS)):
            if action == GLFW_PRESS:
                if key == GLFW_KEY_ESCAPE:
                    self.on_close()


    def on_close(self,window=None):
        self.window_should_close = True

    def close_window(self):
        if self._window:
            glfwDestroyWindow(self._window)
            self._window = None
            self.window_should_close = False


    def update(self,frame,recent_pupil_positions):

        if self.window_should_close:
            self.close_window()

        if self.window_should_open:
            self.open_window()

    def gl_display(self):
        """
        use gl calls to render on world window
        """

        # gl stuff that will show on the world window goes here:

        if self._window:
            self.gl_display_in_window()

    def gl_display_in_window(self):
        active_window = glfwGetCurrentContext()
        glfwMakeContextCurrent(self._window)

        clear_gl_screen()

        # gl stuff that will show on your plugin window goes here

        glfwSwapBuffers(self._window)
        glfwMakeContextCurrent(active_window)



    def cleanup(self):
        """gets called when the plugin get terminated.
        This happends either volunatily or forced.
        if you have an atb bar or glfw window destroy it here.
        """
        if self._window:
            self.close_window()
        self._bar.destroy()

'''

