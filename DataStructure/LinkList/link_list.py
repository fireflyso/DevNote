


class Node:
    
    def __init__(self,value):
        self.value = value
        self.next = 0

# TODO:线程安全
class LinkList:

    def __init__(self):
        self.length = 0
        self.first_node = 0
        self.last_node = 0


    def add(self,value,index = -1):
        if(index < 0):
            self.add_last(value)
        elif(index == 0):
            self.add_first(value)
        elif(index < self.length):
            temp = self.first_node
            for _ in range(index-1):
                temp = temp.next

            new_node = Node(value)
            new_node.next = temp.next
            temp.next = new_node
            
        elif(index == self.length):
            self.add_last(value)
        else:
            print("插入元素位置超出链表长度")


    def add_first(self,value):
        if(self.length == 0):
            self.length = 1
            self.first_node = Node(value)
            self.last_node = self.first_node
        else:
            self.length += 1
            temp = Node(value)
            temp.next = self.first_node
            self.first_node = temp

    def add_last(self,value):
        if(self.length == 0):
            self.add_first(value)
        else:
            self.length += 1
            temp = Node(value)
            self.last_node.next = temp
            self.last_node = temp

    # 删除第index个元素，index参数为空时删除最后一个元素
    def remove(self,index = -1):
        if(index < 0):
            self.remove_last()
        elif(index == 0):
            self.remove_first()
        elif(index < self.length):
            temp = self.first_node
            for _ in range(index-1):
                temp = temp.next
            
            temp.next = temp.next.next
        else:
            print("要删除的元素位置超出链表长度")

    def remove_first(self):
        if(self.length <= 0):
            print("链表为空")
            return
        elif(self.length == 1):
            self.length = 0
            self.first_node = 0
            self.last_node = 0
        else:
            self.first_node = self.first_node.next

    def remove_last(self):
        if(self.length <= 0):
            print("链表为空")
            return
        elif(self.length == 1):
            self.remove_first()
        else:
            temp = self.first_node
            while(temp.next.next != 0):
                temp = temp.next
            temp.next = 0
            self.last_node = temp
        

    def remove_by_value(self,value):
        if(self.length <= 0):
            print("链表为空")
        elif(self.length == 1):
            if(self.first_node.value == value):
                self.length = 0
                self.first_node = 0
                self.last_node = 0
        else:
            temp = self.first_node
            if(temp.value == value):
                self.first_node = temp.next

            while(temp != 0):
                if(temp.next.value == value):
                    temp.next = temp.next.next
                    
                temp = temp.next


    def get_length(self):
        return self.length

    # 检查链表中是否包含某个值，不包含返回False，包含返回True
    def contains_value(self,value):
        if(self.length <= 0):
            print("链表为空")
        else:
            temp = self.first_node
            while(temp != 0):
                if(temp.value == value):
                    return True
                temp = temp.next

            return False

    # 重置第index元素的值
    def reset(self,index,value):
        if(index < 0 or index > self.length):
            print("修改位置超出了链表长度")
            return

        if(self.length <= 0):
            print("链表为空")
            return
        
        temp = self.first_node 
        num = 0
        while(temp != 0):
            num += 1
            if(index == num):
                temp.value = value
                break
            temp = temp.next

    def to_list(self):
        temp_list = []
        temp = self.first_node 
        while(temp != 0):
            temp_list.append(temp.value)
            temp = temp.next

        return temp_list

    def show(self):
        if(self.length == 0):
            print("链表为空")
        elif(self.length == 1):
            print("index : 0  value : {}".format(self.first_node.value))
        else:
            temp = self.first_node
            num = 0
            while(temp != 0):
                print("index : {}  value : {}".format(num,temp.value))
                num += 1
                temp = temp.next
    

if __name__ == '__main__':
    ll = LinkList()
    ll.add("liu")
    ll.add("xu")
    ll.add("lu")
    ll.show()
