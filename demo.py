class Solution(object):
    def dayOfYear(self, date):
        """
        :type date: str
        :rtype: int
        """
        def leap(year):
            if (year % 4) == 0:
                if (year % 100) == 0:
                    if (year % 400) == 0:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        
        leapmonth={
            '01':0,'02':31,'03':31+29,'04':31+29+31,
            '05':31+29+31+30,'06':31+29+31+30+31,
            '07':31+29+31+30+31+30,
            '08':31+29+31+30+31+30+31,
            '09':31+29+31+30+31+30+31+31,
            '10':31+29+31+30+31+30+31+31+30,
            '11':31+29+31+30+31+30+31+31+30+31,
            '12':31+29+31+30+31+30+31+31+30+31+30
        }
        nonleapmonth={
            '01':0,'02':31,'03':31+28,'04':31+28+31,
            '05':31+28+31+30,'06':31+28+31+30+31,
            '07':31+28+31+30+31+30,
            '08':31+28+31+30+31+30+31,
            '09':31+28+31+30+31+30+31+31,
            '10':31+28+31+30+31+30+31+31+30,
            '11':31+28+31+30+31+30+31+31+30+31,
            '12':31+28+31+30+31+30+31+31+30+31+30
        }
        
        day=int(date[-2]+date[-1])
        month=date[5]+date[6]
        year=int(date[0]+date[1]+date[2]+date[3])
        print(year)
        ans=day

        if leap(year)==True:
            print("leap")
            for key,value in leapmonth.items():
                if month==key:
                    ans=ans+value
                    return ans
        else:
            for key,val in nonleapmonth.items():
                print("nonleap")
                if month==key:
                    ans=ans+val
                    return ans


obj=Solution()
a=obj.dayOfYear("2003-03-01")
print(a)