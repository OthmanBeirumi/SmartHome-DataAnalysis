
import csv
import os
import datetime

class Format:
    def __init__(self, data, dataNumber):
        """Arguments: data is the file name, dataNumber is a number"""
        self.data = data
        self.dataNumber = dataNumber
        self.newList = []

    def reading_files(self):
        """Read data from csv files
        :return a list containing lists of measurements"""
        with open(self.data, 'r', encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=",")
            header = next(reader)
            for k in reader:
                if len(k[1]) < 8:
                    k[1] = "0" + k[1]
                self.newList.append(k)

    def dots_to_dash(self):
        """Convert the dots in date into dasher
        :return a list with dashed dates"""
        for i in range(len(self.newList)):
            x = self.newList[i][0].strip(".")
            x = x.replace(".", "-")
            self.newList[i][0] = x
        return self.newList

    def merge_datetime(self):
        """Merge the dashed dates with the time
        add characters to convey with annotated csv files
        :return the list containing the timestamps"""
        for i in range(len(self.newList)):
            x = self.newList[i][0] + "T" + self.newList[i][1] + "Z"
            self.newList[i][0] = x
        return self.newList

    def sorting_list(self, data_list):
        """Sort the data according to the annotated csv files orders
        :return a sorted list"""
        for i in range(len(data_list)):
            table, measure, field, room, type, value, time = i, F"week {self.dataNumber:02d}", data_list[i][2],\
                                                             data_list[i][3], data_list[i][4],data_list[i][5], \
                                                             data_list[i][0]
            self.newList[i][0] = table
            self.newList[i][1] = measure
            self.newList[i][2] = field
            self.newList[i][3] = room
            self.newList[i][4] = type
            self.newList[i][5] = value
            self.newList[i].append(time)
        return self.newList

    def add_spacing(self):
        """Add two empty strings at the beginning to each list
        :return a list of lists with two empty spaces in the first two elements"""
        space = ["", ""]
        for i in range(len(self.newList)):
            x = space + self.newList[i]
            self.newList[i] = x

        return self.newList

    def writing_data(self):
        """Write a new csv file using the formatted list"""
        header1 = ["#group", "FALSE", "FALSE", "TRUE", "TRUE", "TRUE", "TRUE", "FALSE", "FALSE"]
        header2 = ["#datatype",	"string", "long", "string", "string", "string", "string", "double", "dateTime:RFC3339"]
        header3 = ["#default", "_result"]
        header4 = ["", "result", "table", "_measurement", "_field", "room", "type", "_value", "_time"]
        with open(F"week{self.dataNumber:02d}_{self.data}", "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(header1)
            writer.writerow(header2)
            writer.writerow(header3)
            writer.writerow(header4)
            writer.writerows(self.newList)


def main(fn, number):
    file1 = Format(fn, number)
    file1.reading_files()
    file1.dots_to_dash()
    d1 = file1.merge_datetime()
    file1.sorting_list(d1)
    file1.add_spacing()
    file1.writing_data()


if __name__ == '__main__':
    """Read from the directory and check the csv files
     :return csv files only"""
    directory = 'C:/Users/user/PycharmProjects/pythonProject/Sensor_Measurement_Files_Project'
    dirlist = os.listdir(directory)
    t1 = datetime.datetime.now()
    for filename in dirlist:
        if ".csv" in filename:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                main(filename, dirlist.index(filename) + 1)
    t2 = datetime.datetime.now()
    print(F"Elapsed time is: {t2-t1}")