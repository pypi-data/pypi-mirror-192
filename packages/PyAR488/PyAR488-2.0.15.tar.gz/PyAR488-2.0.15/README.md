
package to interact with AR488 interface boards, adds a bit of abstraction to simplify interactions. also can be passed as an argument to custom classes to semplify instrument contorl in your code like :

    from PyAR488.PyAR488 import AR488
    
    class HP3468A:
        def __init__(gpib_addrs:int, interface:AR488):
            self.address = gpib_addrs
            self.interface = interface

        def read_measurement(self):
            self.interface.address(self.address)
            return self.interface.read()


    my_awesome_interface = AR488('COM5')  # open the interface
    my_swesome_meter = HP3468A(22 , my_awesome_interface)  # create the interument object

    reading = my_awesome_meter.read_measurement()  #read measurement
    print(reading)


NOTE : for custom instrument classes remember that the interface must be on the same address as the instrument to comunicate, maybe implement a custom function like:
    
    def _write_bus(messsage:str):
        self.interface.address(self.address):
        self.bus_write(message)
    
This way you are shoure that the interface is always on the right address and the serial command to change is sent only if it is currently configured diferently (so no useless traffic on usb). all is handeled automaticaly in the PyAR488 module.

In case of trouble... enable the Debung on object creation to see printed each and every command sent to the interface and your instruments! 
just use:

    from PyAR488.PyAR488 import AR488
    my_interface = AR488('COM5', debug = True)

this bundle comes with the following instrument libraries:
    HP8660D RF signal source
    HP3325A sweep signal generator
    HP8903A Audio analyzer (with usefull test scripts available on Github
    more to come soon!
