from django import forms #導入form套件

# class PostForm(forms.Form):  #建立類別，需繼承 forms.Form
#     cName = forms.CharField(max_length=20,initial='')
#     cSex = forms.CharField(max_length=2,initial='M')
#     cBirthday = forms.DateField()
#     cEmail = forms.CharField(max_length=100,initial='',required=False)
#     cPhone = forms.CharField(max_length=20,initial='',required=False)
#     cAddr = forms.CharField(max_length=20,initial='',required=False)
# from django import forms
#
class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=2000, widget = forms.Textarea())
# class PostForm(forms.Form):
#     title = forms.CharField(max_length=100, label='標題', min_length=2, error_messages={"min_length": '標題字元段不符合要求！'})
#     content = forms.CharField(widget=forms.Textarea, label='內容')
#     email = forms.EmailField(label='郵箱')
#     reply = forms.BooleanField(required=False, label='回覆')
class YoutubeForm(forms.Form):
    title= forms.CharField(max_length=100, label='', min_length=2,widget=forms.TextInput(attrs={'size':'200'}), error_messages={"min_length": '標題字元段不符合要求！'})



# class PostForm(forms.Form):
#     # error_messages欄位，可以自定義某欄位提交時出現錯誤的時候，顯示的錯誤資訊
#     title = forms.CharField(max_length=100, label='標題', min_length=2, error_messages={"min_length": '標題字元段不符合要求！'})
#     content = forms.CharField(widget=forms.Textarea, label='內容')
#     email = forms.EmailField(label='郵箱')
#     reply = forms.BooleanField(required=False, label='回覆')

