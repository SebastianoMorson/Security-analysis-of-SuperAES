import trsfile
import numpy as np
from scipy.stats import pearsonr
from scipy.spatial.distance import hamming
import matplotlib.pyplot as plt
import re
class AESAttack(object):
    global sbox
    
    sbox= [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

    hamming_weight = [
        0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8
    ]
    global key
    key= [0x21, 0x32, 0x09, 0x21, 0x54, 0x16, 0xA3, 0x67, 0x58, 0x05, 0x11, 0x83, 0x74, 0x97, 0x28, 0x63]



    def read_trs(self):
        plains = [""]*400
        trs = [[]]*400
        for x in range(1,401):
            file = "./Inputs/input_"+str(x)+".txt"
            AESAttack().clean_file(file, 'Generated')
            AESAttack().clean_file(file, 'Using')
            AESAttack().clean_file(file, 'Starting... (0.0%)')
            AESAttack().clean_file(file, 'Warning')
            AESAttack().clean_file(file, '\n')
            AESAttack().clean_file(file, 'Done')
            plain_output = open(file, 'r', encoding='latin-1')
            plain = plain_output.read()
            plains[x-1] = plain
        """
        plains = []
        trs = []
        for file in files:

            plain_output = open(file, 'r', encoding='latin-1')
            plain = plain_output.read()
            if "gêÏÃq" in plain:
                print(ord(plain[15]))
            plains.append(plain)

        """
        plains=np.array(plains)


        for x in range(1,401):
            file = "./Tracce/traccia_"+str(x)+".trs"

            trs_cont = trsfile.open(file)
            trs[x-1] = (trs_cont[0][:47000])

        trs = np.array(trs)
        return plains, trs

    def read_trs_v2(self):
        def clean_file(filename, strtorem):

            with open(filename, 'r') as file_in:
                lines = file_in.readlines()

            with open(filename, 'w') as file_out:
                for line in lines:
                    if not line.startswith(strtorem):
                        file_out.write(line)

        name = "redirect_output"
        clean_file(name, 'Generated')
        clean_file(name, 'Using')
        clean_file(name, 'Starting... (0.0%)')
        clean_file(name, 'Warning')
        clean_file(name, '\n')
        clean_file(name, 'Trace')
        clean_file(name, 'If this')

        plain_output = open(name, 'r')
        plains = plain_output.read()[:-1]
        plains = re.split('\n', plains)  # obtain all the plaintext used for each trace

        plains = np.array(plains)


        file = "test15.trs"

        trs = trsfile.open(file)
        print(np.shape(trs))
        trs = np.array(trs)
        return plains, trs

    def Sbox(self, X):
        y = np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i]=sbox[X[i]]
        return y
    def ADK(self,X, k):
        y = np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i]=X[i]^k
        return y

    def HW(self,X):
        y=np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i]= self.hamming_weight[X[i]]
        return y


    def clean_file(self,filename, strtorem):

        with open(filename, 'r', encoding='latin-1') as file_in:
            lines = file_in.readlines()

        with open(filename, 'w') as file_out:
            for line in lines:
                if not line.startswith(strtorem):
                    file_out.write(line)
    def Initialise(self,N):

        plaintext,trs = AESAttack().read_trs()

        HWguess = np.zeros((16, 256, N)).astype(int)

        for byteno in range(16):
            X = []
            for x in plaintext:

                #if(len(x)!=16 and byteno==15):
                #    X.append(0x0)
                #else:
                X.append(ord(x[byteno]))


            print("byteno={0}\n".format(byteno))
            for kg in range(256):
                Y=AESAttack().ADK(X, kg)
                Y=AESAttack().Sbox(Y)
                HWguess[byteno,kg]=AESAttack().HW(Y)
        return [trs,HWguess, plaintext]

    def maxCorr(self, hw, traces):
        maxcorr=0
        corr=np.zeros(len(traces[0]))
        for i in range(len(traces[0])):

            observation = np.append(hw,traces)
            corr[i] = np.corrcoef(observation, rowvar=False)

            if(abs(corr[i])>maxcorr):
                maxcorr=abs(corr[i])
        return [maxcorr,corr]
    def corrAttack(self,traces,ax,byteno, chunksize, trace_len, n_traces, plaintexts):

        input_bytes = [ord(x[byteno]) for x in plaintexts]
        ax.clear()
        maxkg=0
        maxcorr_k=0
        corr_traces = np.zeros((256, trace_len))
        power_consumption = np.zeros((n_traces, 256))
        keys = np.arange(0,256)


        # add key to the inputs
        add_key = np.zeros((n_traces, 256), dtype=np.uint)
        for i in range(n_traces):
            add_key[i] = list(map(lambda x: input_bytes[i] ^ x, keys))

        ## sub bytes step
        for i in range(n_traces):
            for j in range(256):
                add_key[i][j] = sbox[add_key[i][j]]


        for i in range(n_traces):
            for j in range(256):
                # model hypothesis for the power_consumption
                power_consumption[i][j] = AESAttack().hamming_weight[add_key[i,j]]



        chunks = trace_len//chunksize

        for i in range(0,256):
            print("i:", i)

            for j in range(chunks):
                #print(type(traces[:, j * chunksize:(j + 1) * chunksize]))
                #print(type(power_consumption[:, i:i + 1]))
                observations = np.append(traces[:, j * chunksize:(j + 1) * chunksize],
                                         power_consumption[:, i:i + 1], axis=1)
                # print('obs', observations.shape)
                cmatrix = np.corrcoef(observations, rowvar=False)
                # print(cmatrix.shape)
                corr_traces[i, j * chunksize:(j + 1) * chunksize] = cmatrix[chunksize, 0:chunksize]
        for index in range(256):
            kg = index
            corr = corr_traces[index]
            maxcorr = np.nanmax(corr)
            print(maxcorr)
            if(maxcorr>maxcorr_k):
                maxkg=kg
                maxcorr_k=maxcorr
            if(kg==key[byteno]):
                ax.plot(corr,'r-',alpha=1)
            else:
                ax.plot(corr, color=(0.8, 0.8, 0.8),alpha=0.8)
        ax.set_xlim([1,trace_len])
        
        ax.title.set_text('Byte {0}=0x{1:2x}'.format(byteno,maxkg))
        ax.set_xlabel('Samples')
        ax.set_ylabel(r'$\rho$')

        return maxkg


if __name__ == '__main__':
        [trs,HWguess, plaintext]=AESAttack().Initialise(400)
        n_traces, trace_len = trs.shape
        plt.ion()
        fig = plt.figure()
        ax=[]
        for byteno in range(0,16):
            ax.append(fig.add_subplot(4, 4, byteno+1))

        chunksize = 20


        for byteno in range(0,16):
            print("byte={0}\n".format(byteno))
            AESAttack().corrAttack(trs, ax[byteno], byteno, chunksize, trace_len, n_traces, plaintext)

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.show()
            plt.tight_layout()
            plt.pause(.001)


        plt.ioff()
        plt.show()
