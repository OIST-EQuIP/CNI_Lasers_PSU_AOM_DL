# CNI_Lasers_PSU_AOM_DL

Python driver and widget for CNI Lasers PSU-AOM-DL laser controller.

# Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Requirements

### Driver

Windows (This may work on other OS if you use the right FTDI drivers)  
FTDI CDM drivers (run CDM21216_setup.exe or https://ftdichip.com/drivers/ VCP and D2xx (2.12.28))  
Python 3 (tested using Anaconda 4.11.0 with Python 3.8.12)  
pyvisa  
pyvisa-py  

### Widget

PyQt6    

# Usage

To run the widget, run the CNI_laser_app.py. The usage is self explanitory.  

The driver is CNI_Lasers_PSU_AOM_DL.py

Attributes are:  
_repetition_frequency (int, Hz)  
_current  (int, mA)  
_external_trigger (Boolean)  

Example code:

        import pyvisa as visa
        from CNI_Lasers_PSU_AOM_D import PSU_AOM_DL

        rm = visa.ResourceManager('@py') 
        port = rm.list_resources()[0] # Choose the index that matched the COM port
        laser = PSU_AOM_DL(rm, port)
        
        laser.current = 100 # set current in mA
        print(laser.current) # get current in mA and print
        laser.repetition_frequency = 100 # set repitition frequency in Hz
        print(laser.repetition_frequency # get repetition frequency in Hz and print
        laser.internal_trigger = False # Trigger using internal oscillator
        print(laser.internal_trigger) # get internal trigger boolean and print
        
        laser.port.close()
