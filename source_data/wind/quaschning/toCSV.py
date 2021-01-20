import glob


def dirToCSV(path):

    files = glob.glob(path)

    for file in files:
        input_file = open(file, "r")
        outname = 'pvPower_' + str(file[-9:-4]) + '.csv'        #outname
        output_file = open(outname, 'a')

        for line in input_file.readlines():
            nline = line.replace(',', '.')
            nline = nline.replace('\t', ',')
            output_file.write(nline)

        input_file.close()
        output_file.close()



def dirToCSV1(path):

    files = glob.glob(path)

    for file in files:
        input_file = open(file, "r")
        outname = 'windPower_' + str(file[-9:-4]) + '.csv'
        output_file = open(outname, 'a')

        for line in input_file.readlines():
            nline = line.replace(',', '.')
            line_lst = nline.split('\t')
            if line_lst[0] == 'Summe':
                continue
            # in case field is empty insert 0
            for i, x in enumerate(line_lst):
                if len(x) < 1:
                    line_lst[i] = '0'
            if line_lst[-1] == '\n':
                line_lst[-1] = '0\n'

            nline = ','.join(line_lst)
            output_file.write(nline)

        input_file.close()
        output_file.close()

path = './*.txt'

dirToCSV1(path)