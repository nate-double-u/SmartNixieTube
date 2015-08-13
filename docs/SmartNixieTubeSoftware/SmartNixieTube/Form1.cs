using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.IO;
using System.Web;
using System.Xml;
using System.Threading;

namespace SmartNixieTube
{
    public partial class Form1 : Form
    {
        /* GLOBALS */
        char currentDigit = '-';
        char LDP = 'N';
        char RDP = 'N';
        int anode = 0x80;
        int red = 0x00;
        int green = 0x00;
        int blue = 0x00;
        bool demo = false;
        bool clock = false;
        bool temp = false;
        int demoIndex = 0;
        string city = string.Empty;
        string time = string.Empty;
        string lastTime = string.Empty;

        public void updateCommand()
        {
            tbCommand.Text = "$" + currentDigit + "," + LDP + "," + RDP + "," + anode.ToString().PadLeft(3, '0') + "," + red.ToString().PadLeft(3, '0') + "," + green.ToString().PadLeft(3, '0') + "," + blue.ToString().PadLeft(3, '0');
        }

        public void acpRoutine()
        {
            for (int i = 0; i < 10; i++)
            {
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                serialPort.Write("!");

                Thread.Sleep(25);
            }

            for (int i = 8; i >= 0; i--)
            {
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(i + 0x30);
                updateCommand();
                serialPort.Write(tbCommand.Text);
                serialPort.Write("!");

                Thread.Sleep(25);
            }
        }

        public Form1()
        {
            InitializeComponent();

            foreach (string s in System.IO.Ports.SerialPort.GetPortNames())
            {
                cbPorts.Items.Add(s);
            }

            try
            {
                cbPorts.SelectedIndex = 0;
            }
            catch (Exception)
            {
                MessageBox.Show("No COM ports found");
            }

            updateCommand();
        }

        private void bConnect_Click(object sender, EventArgs e)
        {
            try
            {
                if (serialPort.IsOpen)
                {
                    serialPort.Close();
                }

                serialPort.PortName = cbPorts.SelectedItem.ToString();
                serialPort.BaudRate = 115200;
                serialPort.Parity = System.IO.Ports.Parity.None;
                serialPort.StopBits = System.IO.Ports.StopBits.One;
                serialPort.Open();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void bLDP_Click(object sender, EventArgs e)
        {
            if (LDP == 'Y')
            {
                LDP = 'N';
            }
            else
            {
                LDP = 'Y';
            }

            updateCommand();
        }

        private void bRDP_Click(object sender, EventArgs e)
        {
            if (RDP == 'Y')
            {
                RDP = 'N';
            }
            else
            {
                RDP = 'Y';
            }

            updateCommand();
        }

        private void bClear_Click(object sender, EventArgs e)
        {
            try
            {
                serialPort.Write("@");
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void bLatch_Click(object sender, EventArgs e)
        {
            try
            {
                serialPort.Write("!");
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void bSend_Click(object sender, EventArgs e)
        {
            try
            {
                serialPort.Write(tbCommand.Text);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void trackAnode_Scroll(object sender, EventArgs e)
        {
            anode = trackAnode.Value;
            updateCommand();
        }

        private void trackRed_Scroll(object sender, EventArgs e)
        {
            red = trackRed.Value;
            updateCommand();
        }

        private void trackGreen_Scroll(object sender, EventArgs e)
        {
            green = trackGreen.Value;
            updateCommand();
        }

        private void trackBlue_Scroll(object sender, EventArgs e)
        {
            blue = trackBlue.Value;
            updateCommand();
        }

        private void b0_Click(object sender, EventArgs e)
        {
            currentDigit = '0';
            updateCommand();
        }

        private void b1_Click(object sender, EventArgs e)
        {
            currentDigit = '1';
            updateCommand();
        }

        private void b2_Click(object sender, EventArgs e)
        {
            currentDigit = '2';
            updateCommand();
        }

        private void b3_Click(object sender, EventArgs e)
        {
            currentDigit = '3';
            updateCommand();
        }

        private void b4_Click(object sender, EventArgs e)
        {
            currentDigit = '4';
            updateCommand();
        }

        private void b5_Click(object sender, EventArgs e)
        {
            currentDigit = '5';
            updateCommand();
        }

        private void b6_Click(object sender, EventArgs e)
        {
            currentDigit = '6';
            updateCommand();
        }

        private void b7_Click(object sender, EventArgs e)
        {
            currentDigit = '7';
            updateCommand();
        }

        private void b8_Click(object sender, EventArgs e)
        {
            currentDigit = '8';
            updateCommand();
        }

        private void b9_Click(object sender, EventArgs e)
        {
            currentDigit = '9';
            updateCommand();
        }

        private void bDemo_Click(object sender, EventArgs e)
        {
            if (demo)
            {
                demo = false;
                tDemo.Enabled = false;
            }
            else
            {
                demo = true;
                tDemo.Enabled = true;

                clock = false;
                tClock.Enabled = false;

                temp = false;
            }
        }

        private void bClock_Click(object sender, EventArgs e)
        {
            if (clock)
            {
                clock = false;
                tClock.Enabled = false;
            }
            else
            {
                red = trackRed.Value;
                green = trackGreen.Value;
                blue = trackBlue.Value;
                updateCommand();

                clock = true;
                tClock.Enabled = true;

                demo = false;
                tDemo.Enabled = false;

                temp = false;
            }
        }

        private void tDemo_Tick(object sender, EventArgs e)
        {
            switch (demoIndex++)
            {
                case 0:
                    currentDigit = '0';
                    red = 0xff;
                    green = 0x00;
                    blue = 0x00;
                    break;
                case 1:
                    currentDigit = '1';
                    red = 0x00;
                    green = 0xff;
                    blue = 0x00;
                    break;
                case 2:
                    currentDigit = '2';
                    red = 0x00;
                    green = 0x00;
                    blue = 0xff;
                    break;
                case 3:
                    currentDigit = '3';
                    red = 0xff;
                    green = 0xff;
                    blue = 0x00;
                    break;
                case 4:
                    currentDigit = '4';
                    red = 0x00;
                    green = 0xff;
                    blue = 0xff;
                    break;
                case 5:
                    currentDigit = '5';
                    red = 0xff;
                    green = 0x00;
                    blue = 0xff;
                    break;
                case 6:
                    currentDigit = '6';
                    red = 0x80;
                    green = 0x80;
                    blue = 0x00;
                    break;
                case 7:
                    currentDigit = '7';
                    red = 0x00;
                    green = 0x80;
                    blue = 0x80;
                    break;
                case 8:
                    currentDigit = '8';
                    red = 0x80;
                    green = 0x00;
                    blue = 0x80;
                    break;
                case 9:
                    currentDigit = '9';
                    red = 0xff;
                    green = 0xff;
                    blue = 0xff;
                    demoIndex = 0;
                    break;
                default:
                    break;
            }

            anode = trackAnode.Value;
            updateCommand();

            try
            {
                serialPort.Write(tbCommand.Text);
                serialPort.Write("!");
            }
            catch (Exception ex)
            {
                demo = false;
                tDemo.Enabled = false;
                MessageBox.Show(ex.Message);
            }
        }

        private void tClock_Tick(object sender, EventArgs e)
        {
            time = DateTime.Now.ToString("hh:mm:ss");

            if ((lastTime != time) && (DateTime.Now.Second == 0x00))
            {
                tClock.Stop();
                acpRoutine();
                tClock.Start();
            }

            try
            {
                currentDigit = '-';
                updateCommand();
                serialPort.Write(tbCommand.Text);

                currentDigit = Convert.ToChar(time.Substring(7, 1));
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(time.Substring(6, 1));
                updateCommand();
                serialPort.Write(tbCommand.Text);

                currentDigit = '-';
                updateCommand();
                serialPort.Write(tbCommand.Text);

                currentDigit = Convert.ToChar(time.Substring(4, 1));
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(time.Substring(3, 1));
                updateCommand();
                serialPort.Write(tbCommand.Text);

                currentDigit = '-';
                updateCommand();
                serialPort.Write(tbCommand.Text);

                currentDigit = Convert.ToChar(time.Substring(1, 1));
                updateCommand();
                serialPort.Write(tbCommand.Text);
                currentDigit = Convert.ToChar(time.Substring(0, 1));
                updateCommand();
                serialPort.Write(tbCommand.Text);

                currentDigit = '-';
                updateCommand();
                serialPort.Write(tbCommand.Text);

                serialPort.Write("!");

                lastTime = time;
            }
            catch (Exception ex)
            {
                clock = false;
                tClock.Enabled = false;
                MessageBox.Show(ex.Message);
            }
        }
    }
}