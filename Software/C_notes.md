# 1. C
## 1.1. 参考资料
- C语言程序设计第四版 谭浩强
## 1.2. 总结：
这个是比较系统的笔记，根据C语言程序设计第四版：[笔记：C语言程序设计第四版](https://github.com/SuperChange001/hw_learning_material/raw/master/PDF/C语言程序设计第四版%20谭浩强.pdf) 
下面是一些比较零散的记录。   

- 函数入栈都是右传递：就是右边的参数先调用
	- C的所有运算是右结合的。运算从右边开始算
4. 函数形参的传递：
   1. 变量：传值
   2. 数组：传递的是实参的地址，形参的数组长度可以缺省，类型不能省略
- 所有的参数都是传值传递，不是传递的本身
	- 所以，修改一个变量，要传入指针
	- 修改一个指针，要传入指针的指针
- 语句块：{}
	- 代表了一个作用域，可以定义临时变量，结束了就会释放
- i++和++i
	- i++：先把这样语句的所有其他操作都做了，然后i+1
	- ++i：先i+1,然后再做这个语句的其他操作
- 为什么需要指针？
	- C语言的形参是传值。
	- 常规变量：只是把值传递给被调函数。改不了这个变量在主调函数的值
	- 一级指针变量：把指针变量的指针（指向的addr）传递进去了。可以在被调函数里改变指针指向地址的值。就是传入&a，可以改变a
	- 二级指针变量：被指向一个一级指针变量addr的指针传递进去了。可以在被调函数里改变这个一级指针变量的指针指向。就是传入&p，可以改变p
- 野指针：指向了意外的地址的指针
   1. 因为原先函数在stack的内存回收，把这个函数的临时内存传出去会变成野指针
   2. 释放了一段内存空间，但是指针还是指向他，没有改为指向NULL

9. 数组类型的数据：
	1. 本质是个指针，但是个常量指针，所以不能直接对数组指针直接赋值。和普通的指针变量是不一样的
   	1. 数组数据：存在暂存区，不是简简单单的一个指针
   	2. 数据内的数据可以随意修改，这个就说明了数组不是简单地指向常量区

# 2. 数据类型：
数据类型的本质：告诉computer接下来要存储的数据是多大的，应该怎么解析这个数据   
以下是基本整数关键词：
• char: 有符号 8 位整数。
• short: 有符号 16 位整数。
• int: 有符号 32 位整数。
• long: 在 32 位系统是 32 整数 (long int)，在 64 位系统则是 64 位整数。
• long long: 有符号 64 位整数 (long long int)。
• bool: _Bool 类型， 8 位整数，在 stdbool.h 中定义了 bool / true / false 宏便于使⽤用。


|     Name     | Meaning | Length | Range | range |          |
| ------------ | ------- | ------ | ----- | ----- | -------- |
| int          |         | 4      |       |       | %d       |
| Unsigned int |         | 4      |       |       | %u       |
| u8           |         | 1      |       |       | %u       |
| U32          |         | 4      |       |       | %u       |
| char         |         | 1      |       |       | %c       |
| float        |         | 4      |       |       | %f       |
| short        |         | 2      |       |       | %hd  %hu |
| Long         |         | 8      |       |       | %ld  %lu |
| Double       |         | 8      |       |       | %f       |
| Pointer      |         |        |       |       | %p       |

## 2.1. 尾缀：
我们可以⽤用不同的后缀来表⽰示整数常量类型。
```
printf("int size=%d;\n", sizeof(1));
printf("unsigned int size=%d;\n", sizeof(1U));
printf("long size=%d;\n", sizeof(1L));
printf("unsigned long size=%d;\n", sizeof(1UL));
printf("long long size=%d;\n", sizeof(1LL));
printf("unsigned long long size=%d;\n", sizeof(1ULL));
//输出:
int size=4;
unsigned int size=4;
long size=4;
unsigned long size=4;
long long size=8;
unsigned long long size=8;
```

## 2.2. 浮点数：
C 提供了不同精度的浮点。
• float: 32 位 4 字节浮点数，精确度 6。
• double: 64 位 8 字节浮点数，精确度 15。
• long double: 80 位 10 字节浮点数，精确度 19 位。
浮点数默认类型是 double，可以添加后缀 F 来表⽰示 float， L 表⽰示 long double，可以局部省略。
```
printf("float %f size=%d\n", 1.F, sizeof(1.F));
printf("double %f size=%d\n", .123, sizeof(.123));
printf("long double %Lf size=%d\n", 1.234L, sizeof(1.234L));
//输出:
float 1.000000 size=4
double 0.123000 size=8
long double 1.234000 size=12 # 对⻬齐
```

## 2.3. 进制：
```
int x = 010;
int y = 0x0A;
printf("x = %d, y = %d\n", x, y);
//输出:
x = 8, y = 10
```

# 3. 优先级
图：![](https://gitee.com/AndrewChu/markdown/raw/master/1598597614_20200811230529036_1200137028.png)


# 4. 关键字的作用：
1. const：常量标志
    - 行参：不会改变传入的指针
    - const char * s：*s是一个变量，所以是个常量指针。说明指针对应的值不会变。
    - char const * s：*s是一个变量，所以是个常量指针。说明指针对应的值不会变。
    - char * const s：s是一个指针，所以是指针常量。说明指向不会变

2. 全局变量：是存放在静态存储区（都是放在内存中）
2. static是静态变量，是存放在静态存储区（都是放在内存中），
   1. 是在编译的时候赋初始值，一般变量是在函数调用的时候赋值
   2. 不会随着函数的回收而销毁
   3.  会一直存在且只初始化一次。
   4. 以后的调用是直接拿来用，***不会再赋值***
   5. 外部定义的static变量***不能被外部函数调用***
3. register变量，是存放在cpu的寄存器中，可以提高效率。不用每次从memory里读数据后再处理。
4. extern： 告诉编译器，变量在其他地方定义，这里是直接引用








# 5. 数组

## 5.1. 一维数组

数组的名字就是数据储存的指针

```c
int num[]={1,2,3,4,5};
int *p;
//num[0] == 1
//p = num
```

## 5.2. 二维数组

1. 二维数据实际上是指向指针的指针
2. 数组名是第一个元素的地址
3. 数组名+1，步进是数组一行的长度
4. *(数组名+1), 返回的还是指针，不过已经是指向第1行的指针，也是第一行指针的初始地址
5. `*(*(数组名+1)+2`第一行，第二列的元素

```c
int num[][3]={{1,2,3},{4,5,6}};
int *p[3];//3个元素的指针，步进为4
int (*p2)[3];//一个内容为3个int的指针，步进为3*4
p2 = num 
//num[0][2] == 3
//`*(*(p2+1)+2`  == 6
```
## 5.3. 数组取值
图：![未命名.001](https://gitee.com/AndrewChu/markdown/raw/master/1598597419_未命名.001.jpg)

1. 指针变量和一般变量的区别：
   1. 指针变量内存的是地址，
   2. 一般变量内存的是变量的值
2. 指针和指针变量：
   2. ***指针变量：这个指针的变量名字。他有自己的内存地址和值（指针，就是目标地址）***  
   2. ***指针：就是目标的地址*** 
   3. 两者其实是一个东西，但是逻辑思考的路径不一样
3. 指针操作
   1. `*` 取值操作，用于指针，取出指针里的值，是目标地址的值
   2. `&`取址操作，用于变量，取出这个变量的内存地址
# 6. 指针

```c
    int main(void){
        int *p1 = NULL;
        int *p2 = NULL;
        int i = 0;
        p1 = (int *)malloc(200);
        strcpy(p1,"123456789000asdfads");
        for(i=0;i<10;i++){
            p2 = p1 + i;
            printf("%c", *p2);
        }
    }
```

图：![Screenshot-2019-11-12PM6.27.03](https://gitee.com/AndrewChu/markdown/raw/master/1598597418_Screenshot-2019-11-12PM6.27.03.png)

## 6.1. 字符串一级指针图

> 指针变量p++，其实是指针值+1个单位。不是指针变量存放的地址+1。
>
> 记住：对一个变量做操作，是不会操作到他本身的，只会操作到他储存的数据

图：![Screenshot-2019-11-12PM8.08.28](https://gitee.com/AndrewChu/markdown/raw/master/1598597418_Screenshot-2019-11-12PM8.08.28.png)

```c
// copy demo
#include <stdio.h>

void cp2array(char *from, char *to){
    for (; *from != '\0'; from++, to++) {
            *to = *from;
    }
    *to = '\0';
}

int main(void){
    char *from = "Hello World";
    char num[100];
    cp2array(from, num);
    printf("value: %s", num);
}
```

图：![Screenshot-2019-11-12PM8.42.53](https://gitee.com/AndrewChu/markdown/raw/master/1598597419_Screenshot-2019-11-12PM8.42.53.png)


# 7. 结构体

```c
struct date{
  int month;
  int day;
  int year;
} birthday;

struct student{
	int num;
	char *name;
	char score;
  struct date birthday;
}boy1,boy2;

boy1.num=007;
boy1.name="andrew";
boy1.birthday.day = 1; 
boy2 = boy1;
```

## 7.1. 动态存储分配

1. malloc：在动态存储区中分配一个长度为size的连续空间，返回void类型的指针
2. Calloc: 分配n个长度为size的连续空间，返回void类型的指针
3. free: 输入指针，释放这个空间

## 7.2. 链表 

动态地分配地址的结构

图：![Screenshot-2019-11-11PM7.51.14](https://gitee.com/AndrewChu/markdown/raw/master/1598597415_Screenshot-2019-11-11PM7.51.14.png)

```c
// 静态的链表
#include <stdio.h>

struct student{
    long id;
    float score;
    struct student *next;
};

void main(void){
    struct student s1,s2,s3,*head;
    s1.id = 1;
    s1.score = 100;
    s2.id = 2;
    s2.score = 99;
    s3.id = 3;
    s3.score = 98;

    head = &s1;
    s1.next = &s2;
    s2.next = &s3;
    s3.next = NULL;

    do{
        printf("%ld %5.1f\n", head->id,head->score);
        head = head->next;
    }while (head);

}
```

## 7.3. 枚举

```c
enum weekday {sun,mon,tue}a,b,c;
```

## 7.4. typedef

已知类型名，换个名字

```c
typedef int INT;

typedef struct{
  int id;
  char *name;
}Student;
Student s1;
```

# 8. 文件

```c
FILE *fp;			
fp = fopen(file_name, method);
fclose(fp)
```

图：![Screenshot-2019-11-12AM10](https://gitee.com/AndrewChu/markdown/raw/master/1598597515_20200828145148918_1686613444.png)


# 9. 内存
## 9.1. 内存四区

> 1. heap 堆：系统分配，整个程序退出才会销毁
> 2. stack 栈： 临时变量，用完就会销毁
> 3. 全局变量区：字符串常量存储的地方，不能改写里面的数据
> 4. 代码区：用户的代码

图：![Screenshot-2019-11-12PM3.15.24](https://gitee.com/AndrewChu/markdown/raw/master/1598597417_Screenshot-2019-11-12PM3.15.24.png)






# 10. exercise

```c
#include <stdio.h>
#include <strings.h>

// trim the space in the string
int trimSpace(char *inbuf, char *outbuf){
    char *inbufTemp = inbuf;
    if(inbuf == NULL || outbuf == NULL){
        printf("error 1");
        return -1;
    }

    while (*inbufTemp != '\0'){
        if (*inbufTemp != ' '){
            *outbuf++ = *inbufTemp++;
        }
        else{
            inbufTemp++;
        }
    }
    *outbuf = '\0';
    return 0;
}

// separate the even and odd number
int getNumStr(char *source, char *bufE, char *bufO){
    char *sourceTemp = source;
    if (source == NULL || bufE == NULL || bufO == NULL){
        printf("error 2");
        return -1;
    }
    while(*sourceTemp != '\0'){
        if (*sourceTemp>=48 && *sourceTemp<=57){
            if((*sourceTemp-48)%2){
                *bufE++ = *sourceTemp++;
            } else{
                *bufO++ = *sourceTemp++;
            }
        } else{
            sourceTemp++;
        }
    }
    *bufE = '\0';
    *bufO = '\0';
    return 0;
}

int getKeyByValue(char *keyValueBuf, char *keyBuf, char *valueBuf ,int *lenP){
    char *keyValueBufTemp = keyValueBuf;
    char temp[strlen(keyValueBuf)];
    int i;
    if (keyValueBuf ==NULL || keyBuf == NULL || valueBuf == NULL){
        printf("error 3");
        return -1;
    }

    if (keyValueBufTemp = strstr(keyValueBufTemp,keyBuf)){
        keyValueBufTemp += strlen(keyBuf);
        trimSpace(keyValueBufTemp, temp);
        for(i=1;i<=strlen(temp);i++){
            *valueBuf++ = *(temp+i);
        }
        return 0;
    }else {
        printf("None key found");
        return -1;
    }
}
int main(void){
    char *str1 = "    abcdddd    1";
    char out1[strlen(str1)];
    trimSpace(str1, out1);
    printf("value: %s\n\r", out1);

    char *str2 = "11a22b30d41z";
    char bufE[strlen(str2)];
    char bufO[strlen(str2)];
    getNumStr(str2, bufE, bufO);
    printf("Even: %s || Odd:%s\n\r", bufE, bufO);

    char *str3 = "key1= andrew     ";
    char *keyP = "key1";
    char valueBuf[strlen(str3)];
    int len=0;
    getKeyByValue(str3, keyP, valueBuf, &len);
    printf("Value: %s\n\r", valueBuf);

}

```
