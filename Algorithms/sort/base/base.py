

class Base:

    sort_arr = [23,5,8,122,32,45,72,342,2,89,12,34,11,9,77]

    def swap(self,a,b):
        temp = self.sort_arr[a]
        self.sort_arr[a] = self.sort_arr[b]
        self.sort_arr[b] = temp