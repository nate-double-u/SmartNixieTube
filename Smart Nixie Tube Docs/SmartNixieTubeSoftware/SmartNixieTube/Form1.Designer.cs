namespace SmartNixieTube
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.bConnect = new System.Windows.Forms.Button();
            this.cbPorts = new System.Windows.Forms.ComboBox();
            this.serialPort = new System.IO.Ports.SerialPort(this.components);
            this.b7 = new System.Windows.Forms.Button();
            this.b8 = new System.Windows.Forms.Button();
            this.b9 = new System.Windows.Forms.Button();
            this.b4 = new System.Windows.Forms.Button();
            this.b5 = new System.Windows.Forms.Button();
            this.b6 = new System.Windows.Forms.Button();
            this.b1 = new System.Windows.Forms.Button();
            this.b2 = new System.Windows.Forms.Button();
            this.b3 = new System.Windows.Forms.Button();
            this.bLDP = new System.Windows.Forms.Button();
            this.b0 = new System.Windows.Forms.Button();
            this.bRDP = new System.Windows.Forms.Button();
            this.bClear = new System.Windows.Forms.Button();
            this.bLatch = new System.Windows.Forms.Button();
            this.tbCommand = new System.Windows.Forms.TextBox();
            this.bSend = new System.Windows.Forms.Button();
            this.trackAnode = new System.Windows.Forms.TrackBar();
            this.trackRed = new System.Windows.Forms.TrackBar();
            this.trackGreen = new System.Windows.Forms.TrackBar();
            this.trackBlue = new System.Windows.Forms.TrackBar();
            this.bDemo = new System.Windows.Forms.Button();
            this.tDemo = new System.Windows.Forms.Timer(this.components);
            this.bClock = new System.Windows.Forms.Button();
            this.tClock = new System.Windows.Forms.Timer(this.components);
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.trackAnode)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackRed)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackGreen)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBlue)).BeginInit();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.bConnect);
            this.groupBox1.Controls.Add(this.cbPorts);
            this.groupBox1.Location = new System.Drawing.Point(12, 12);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(90, 77);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "COM Port";
            // 
            // bConnect
            // 
            this.bConnect.Location = new System.Drawing.Point(6, 46);
            this.bConnect.Name = "bConnect";
            this.bConnect.Size = new System.Drawing.Size(75, 23);
            this.bConnect.TabIndex = 1;
            this.bConnect.Text = "Connect";
            this.bConnect.UseVisualStyleBackColor = true;
            this.bConnect.Click += new System.EventHandler(this.bConnect_Click);
            // 
            // cbPorts
            // 
            this.cbPorts.FormattingEnabled = true;
            this.cbPorts.Location = new System.Drawing.Point(6, 19);
            this.cbPorts.Name = "cbPorts";
            this.cbPorts.Size = new System.Drawing.Size(75, 21);
            this.cbPorts.TabIndex = 0;
            // 
            // b7
            // 
            this.b7.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b7.Location = new System.Drawing.Point(108, 17);
            this.b7.Name = "b7";
            this.b7.Size = new System.Drawing.Size(77, 72);
            this.b7.TabIndex = 1;
            this.b7.Text = "7";
            this.b7.UseVisualStyleBackColor = true;
            this.b7.Click += new System.EventHandler(this.b7_Click);
            // 
            // b8
            // 
            this.b8.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b8.Location = new System.Drawing.Point(191, 17);
            this.b8.Name = "b8";
            this.b8.Size = new System.Drawing.Size(77, 72);
            this.b8.TabIndex = 2;
            this.b8.Text = "8";
            this.b8.UseVisualStyleBackColor = true;
            this.b8.Click += new System.EventHandler(this.b8_Click);
            // 
            // b9
            // 
            this.b9.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b9.Location = new System.Drawing.Point(274, 17);
            this.b9.Name = "b9";
            this.b9.Size = new System.Drawing.Size(77, 72);
            this.b9.TabIndex = 3;
            this.b9.Text = "9";
            this.b9.UseVisualStyleBackColor = true;
            this.b9.Click += new System.EventHandler(this.b9_Click);
            // 
            // b4
            // 
            this.b4.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b4.Location = new System.Drawing.Point(108, 95);
            this.b4.Name = "b4";
            this.b4.Size = new System.Drawing.Size(77, 72);
            this.b4.TabIndex = 4;
            this.b4.Text = "4";
            this.b4.UseVisualStyleBackColor = true;
            this.b4.Click += new System.EventHandler(this.b4_Click);
            // 
            // b5
            // 
            this.b5.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b5.Location = new System.Drawing.Point(191, 95);
            this.b5.Name = "b5";
            this.b5.Size = new System.Drawing.Size(77, 72);
            this.b5.TabIndex = 5;
            this.b5.Text = "5";
            this.b5.UseVisualStyleBackColor = true;
            this.b5.Click += new System.EventHandler(this.b5_Click);
            // 
            // b6
            // 
            this.b6.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b6.Location = new System.Drawing.Point(274, 95);
            this.b6.Name = "b6";
            this.b6.Size = new System.Drawing.Size(77, 72);
            this.b6.TabIndex = 6;
            this.b6.Text = "6";
            this.b6.UseVisualStyleBackColor = true;
            this.b6.Click += new System.EventHandler(this.b6_Click);
            // 
            // b1
            // 
            this.b1.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.b1.Location = new System.Drawing.Point(108, 173);
            this.b1.Name = "b1";
            this.b1.Size = new System.Drawing.Size(77, 72);
            this.b1.TabIndex = 7;
            this.b1.Text = "1";
            this.b1.UseVisualStyleBackColor = true;
            this.b1.Click += new System.EventHandler(this.b1_Click);
            // 
            // b2
            // 
            this.b2.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b2.Location = new System.Drawing.Point(191, 173);
            this.b2.Name = "b2";
            this.b2.Size = new System.Drawing.Size(77, 72);
            this.b2.TabIndex = 8;
            this.b2.Text = "2";
            this.b2.UseVisualStyleBackColor = true;
            this.b2.Click += new System.EventHandler(this.b2_Click);
            // 
            // b3
            // 
            this.b3.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b3.Location = new System.Drawing.Point(274, 173);
            this.b3.Name = "b3";
            this.b3.Size = new System.Drawing.Size(77, 72);
            this.b3.TabIndex = 9;
            this.b3.Text = "3";
            this.b3.UseVisualStyleBackColor = true;
            this.b3.Click += new System.EventHandler(this.b3_Click);
            // 
            // bLDP
            // 
            this.bLDP.Font = new System.Drawing.Font("Microsoft Sans Serif", 19F);
            this.bLDP.Location = new System.Drawing.Point(108, 251);
            this.bLDP.Name = "bLDP";
            this.bLDP.Size = new System.Drawing.Size(77, 72);
            this.bLDP.TabIndex = 10;
            this.bLDP.Text = "LDP";
            this.bLDP.UseVisualStyleBackColor = true;
            this.bLDP.Click += new System.EventHandler(this.bLDP_Click);
            // 
            // b0
            // 
            this.b0.Font = new System.Drawing.Font("Microsoft Sans Serif", 36F);
            this.b0.Location = new System.Drawing.Point(191, 251);
            this.b0.Name = "b0";
            this.b0.Size = new System.Drawing.Size(77, 72);
            this.b0.TabIndex = 11;
            this.b0.Text = "0";
            this.b0.UseVisualStyleBackColor = true;
            this.b0.Click += new System.EventHandler(this.b0_Click);
            // 
            // bRDP
            // 
            this.bRDP.Font = new System.Drawing.Font("Microsoft Sans Serif", 19F);
            this.bRDP.Location = new System.Drawing.Point(274, 251);
            this.bRDP.Name = "bRDP";
            this.bRDP.Size = new System.Drawing.Size(77, 72);
            this.bRDP.TabIndex = 12;
            this.bRDP.Text = "RDP";
            this.bRDP.UseVisualStyleBackColor = true;
            this.bRDP.Click += new System.EventHandler(this.bRDP_Click);
            // 
            // bClear
            // 
            this.bClear.Font = new System.Drawing.Font("Microsoft Sans Serif", 16F);
            this.bClear.Location = new System.Drawing.Point(18, 95);
            this.bClear.Name = "bClear";
            this.bClear.Size = new System.Drawing.Size(77, 72);
            this.bClear.TabIndex = 13;
            this.bClear.Text = "Clear";
            this.bClear.UseVisualStyleBackColor = true;
            this.bClear.Click += new System.EventHandler(this.bClear_Click);
            // 
            // bLatch
            // 
            this.bLatch.Font = new System.Drawing.Font("Microsoft Sans Serif", 16F);
            this.bLatch.Location = new System.Drawing.Point(18, 251);
            this.bLatch.Name = "bLatch";
            this.bLatch.Size = new System.Drawing.Size(77, 72);
            this.bLatch.TabIndex = 14;
            this.bLatch.Text = "Latch";
            this.bLatch.UseVisualStyleBackColor = true;
            this.bLatch.Click += new System.EventHandler(this.bLatch_Click);
            // 
            // tbCommand
            // 
            this.tbCommand.Location = new System.Drawing.Point(18, 335);
            this.tbCommand.Name = "tbCommand";
            this.tbCommand.ReadOnly = true;
            this.tbCommand.Size = new System.Drawing.Size(333, 20);
            this.tbCommand.TabIndex = 15;
            this.tbCommand.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // bSend
            // 
            this.bSend.Font = new System.Drawing.Font("Microsoft Sans Serif", 16F);
            this.bSend.Location = new System.Drawing.Point(18, 173);
            this.bSend.Name = "bSend";
            this.bSend.Size = new System.Drawing.Size(77, 72);
            this.bSend.TabIndex = 16;
            this.bSend.Text = "Send";
            this.bSend.UseVisualStyleBackColor = true;
            this.bSend.Click += new System.EventHandler(this.bSend_Click);
            // 
            // trackAnode
            // 
            this.trackAnode.Location = new System.Drawing.Point(357, 157);
            this.trackAnode.Maximum = 255;
            this.trackAnode.Name = "trackAnode";
            this.trackAnode.Size = new System.Drawing.Size(333, 45);
            this.trackAnode.TabIndex = 17;
            this.trackAnode.TickStyle = System.Windows.Forms.TickStyle.None;
            this.trackAnode.Value = 128;
            this.trackAnode.Scroll += new System.EventHandler(this.trackAnode_Scroll);
            // 
            // trackRed
            // 
            this.trackRed.BackColor = System.Drawing.Color.Red;
            this.trackRed.Location = new System.Drawing.Point(357, 208);
            this.trackRed.Maximum = 255;
            this.trackRed.Name = "trackRed";
            this.trackRed.Size = new System.Drawing.Size(333, 45);
            this.trackRed.TabIndex = 18;
            this.trackRed.TickStyle = System.Windows.Forms.TickStyle.None;
            this.trackRed.Scroll += new System.EventHandler(this.trackRed_Scroll);
            // 
            // trackGreen
            // 
            this.trackGreen.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(192)))), ((int)(((byte)(0)))));
            this.trackGreen.Location = new System.Drawing.Point(357, 259);
            this.trackGreen.Maximum = 255;
            this.trackGreen.Name = "trackGreen";
            this.trackGreen.Size = new System.Drawing.Size(333, 45);
            this.trackGreen.TabIndex = 19;
            this.trackGreen.TickStyle = System.Windows.Forms.TickStyle.None;
            this.trackGreen.Scroll += new System.EventHandler(this.trackGreen_Scroll);
            // 
            // trackBlue
            // 
            this.trackBlue.BackColor = System.Drawing.Color.Blue;
            this.trackBlue.Location = new System.Drawing.Point(357, 310);
            this.trackBlue.Maximum = 255;
            this.trackBlue.Name = "trackBlue";
            this.trackBlue.Size = new System.Drawing.Size(333, 45);
            this.trackBlue.TabIndex = 20;
            this.trackBlue.TickStyle = System.Windows.Forms.TickStyle.None;
            this.trackBlue.Scroll += new System.EventHandler(this.trackBlue_Scroll);
            // 
            // bDemo
            // 
            this.bDemo.Font = new System.Drawing.Font("Microsoft Sans Serif", 30F);
            this.bDemo.Location = new System.Drawing.Point(357, 17);
            this.bDemo.Name = "bDemo";
            this.bDemo.Size = new System.Drawing.Size(333, 64);
            this.bDemo.TabIndex = 21;
            this.bDemo.Text = "Demo";
            this.bDemo.UseVisualStyleBackColor = true;
            this.bDemo.Click += new System.EventHandler(this.bDemo_Click);
            // 
            // tDemo
            // 
            this.tDemo.Interval = 1000;
            this.tDemo.Tick += new System.EventHandler(this.tDemo_Tick);
            // 
            // bClock
            // 
            this.bClock.Font = new System.Drawing.Font("Microsoft Sans Serif", 30F);
            this.bClock.Location = new System.Drawing.Point(357, 87);
            this.bClock.Name = "bClock";
            this.bClock.Size = new System.Drawing.Size(333, 64);
            this.bClock.TabIndex = 22;
            this.bClock.Text = "Clock";
            this.bClock.UseVisualStyleBackColor = true;
            this.bClock.Click += new System.EventHandler(this.bClock_Click);
            // 
            // tClock
            // 
            this.tClock.Interval = 500;
            this.tClock.Tick += new System.EventHandler(this.tClock_Tick);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(492, 180);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(56, 13);
            this.label1.TabIndex = 23;
            this.label1.Text = "Brightness";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.BackColor = System.Drawing.Color.Red;
            this.label2.Location = new System.Drawing.Point(504, 231);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(27, 13);
            this.label2.TabIndex = 24;
            this.label2.Text = "Red";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(192)))), ((int)(((byte)(0)))));
            this.label3.Location = new System.Drawing.Point(499, 282);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(36, 13);
            this.label3.TabIndex = 25;
            this.label3.Text = "Green";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.BackColor = System.Drawing.Color.Blue;
            this.label4.ForeColor = System.Drawing.Color.White;
            this.label4.Location = new System.Drawing.Point(503, 333);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(28, 13);
            this.label4.TabIndex = 26;
            this.label4.Text = "Blue";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(703, 371);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.bClock);
            this.Controls.Add(this.bDemo);
            this.Controls.Add(this.trackBlue);
            this.Controls.Add(this.trackGreen);
            this.Controls.Add(this.trackRed);
            this.Controls.Add(this.trackAnode);
            this.Controls.Add(this.bSend);
            this.Controls.Add(this.tbCommand);
            this.Controls.Add(this.bLatch);
            this.Controls.Add(this.bClear);
            this.Controls.Add(this.bRDP);
            this.Controls.Add(this.b0);
            this.Controls.Add(this.bLDP);
            this.Controls.Add(this.b3);
            this.Controls.Add(this.b2);
            this.Controls.Add(this.b1);
            this.Controls.Add(this.b6);
            this.Controls.Add(this.b5);
            this.Controls.Add(this.b4);
            this.Controls.Add(this.b9);
            this.Controls.Add(this.b8);
            this.Controls.Add(this.b7);
            this.Controls.Add(this.groupBox1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Form1";
            this.Text = "Smart Nixie Tube";
            this.groupBox1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.trackAnode)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackRed)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackGreen)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBlue)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.ComboBox cbPorts;
        private System.Windows.Forms.Button bConnect;
        private System.IO.Ports.SerialPort serialPort;
        private System.Windows.Forms.Button b7;
        private System.Windows.Forms.Button b8;
        private System.Windows.Forms.Button b9;
        private System.Windows.Forms.Button b4;
        private System.Windows.Forms.Button b5;
        private System.Windows.Forms.Button b6;
        private System.Windows.Forms.Button b1;
        private System.Windows.Forms.Button b2;
        private System.Windows.Forms.Button b3;
        private System.Windows.Forms.Button bLDP;
        private System.Windows.Forms.Button b0;
        private System.Windows.Forms.Button bRDP;
        private System.Windows.Forms.Button bClear;
        private System.Windows.Forms.Button bLatch;
        private System.Windows.Forms.TextBox tbCommand;
        private System.Windows.Forms.Button bSend;
        private System.Windows.Forms.TrackBar trackAnode;
        private System.Windows.Forms.TrackBar trackRed;
        private System.Windows.Forms.TrackBar trackGreen;
        private System.Windows.Forms.TrackBar trackBlue;
        private System.Windows.Forms.Button bDemo;
        private System.Windows.Forms.Timer tDemo;
        private System.Windows.Forms.Button bClock;
        private System.Windows.Forms.Timer tClock;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
    }
}

