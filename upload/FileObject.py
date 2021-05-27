import pandas as pd
import re

class StudentFile:

  def __init__(self,file):
      self.df = pd.read_excel(file)
      self.col_format= ['Sr. No', 'Batch', 'First Name', 'Last Name', 'Email','Contact']


  def validate_file(self):
      col_format=self.col_format
      df=self.df

      answer=self.check_col_header()

      if(answer[0]=="correct"):
          print("col header correct")
          pass
      else:
          final_answer=["col header wrong",answer]
          return final_answer

      for col in col_format:
          validated = df.apply(
              lambda x: self.check_col(x['Sr. No'], x[col], col)[0], axis=1)
          sno = df.apply(lambda x: self.check_col(x['Sr. No'], x[col], col)[1],axis=1)
          value = df.apply(lambda x: self.check_col(x['Sr. No'], x[col], col)[2],axis=1)

          checked_df = pd.DataFrame({'validated': validated, 'sno': sno, 'value': value})

          wrong_sno = list(
              checked_df[checked_df['validated'] == "Wrong"]['sno'])
          wrong_value = list(
              checked_df[checked_df['validated'] == "Wrong"]['value'])
          wrong_df = pd.DataFrame(
              {'wrong_sno': wrong_sno, 'wrong_value': wrong_value})

          wrong_df.fillna('',inplace=True)

          wrong_dfT = wrong_df.T.to_dict()
          wrong_df_list = []
          for i in wrong_dfT:
              wrong_df_list.append(wrong_dfT[i])

          empty_sno = list(
              checked_df[checked_df['validated'] == "Empty"]['sno'])
          empty_value = list(
              checked_df[checked_df['validated'] == "Empty"]['value'])
          empty_df = pd.DataFrame(
              {'empty_sno': empty_sno, 'empty_value': empty_value})

          empty_df.fillna('',inplace=True)

          empty_dfT = empty_df.T.to_dict()
          empty_df_list = []
          for i in empty_dfT:
              empty_df_list.append(empty_dfT[i])

          if( (len(wrong_sno)==0) and (len(empty_sno)==0) ):
              print(col," is correct")

          elif ((len(wrong_sno) != 0) and (len(empty_sno) == 0)):
              final_answer=["wrong col",[col,wrong_df_list,self.format_rule(col)]]
              return final_answer

          elif ((len(wrong_sno) == 0) and (len(empty_sno) != 0)):
              final_answer=["empty col",[col,empty_df_list]]
              return final_answer

          elif ((len(wrong_sno) != 0) and (len(empty_sno) != 0)):
              final_answer=["empty & wrong col",[col,wrong_df_list,empty_df_list,self.format_rule(col)]]
              return final_answer

          if(col=='Sr. No'):
              if not(df[col].is_unique):
                  final_answer=["sno not unique",[list(df[df.duplicated(subset=col)][col])]]
                  return final_answer


      final_answer=["everything correct",[]]
      return final_answer









  def check_col_header(self):
      df=self.df
      count = 0
      wrong_col = None
      col_uploaded = list(df.columns)
      col_format = self.col_format
      extra = False

      for cols in col_uploaded:
          if (count > len(col_format) - 1):
              extra = True
              extra_list = col_uploaded[col_uploaded.index(cols):]
              break
          if (cols == col_format[count]):
              pass
          else:
              expected_col = col_format[count]
              wrong_col = col_uploaded[count]
              break
          count += 1

      if (extra == True):
          answer=["extra",extra_list]
          print("The following columns are mentioned in your file" + str(
              extra_list) + " but is not present in the format")
      elif ((wrong_col is None) and (count == len(col_format))):
          answer=["correct",[]]
          print("All column name were as per the format")
      elif ((wrong_col is None) and (count < len(col_format))):
          answer=["missing",col_format[count:]]
          print("The following columns name are missing- " + str(
              col_format[count:]))
      else:
          answer=["wrong",[expected_col,count+1,wrong_col]]
          print(
              "Expected column heading to be (" + expected_col + ") at position no " + str(
                  count + 1) + ". But got column (" + wrong_col + ") instead")

      return answer



  def check_col(self,sno, value, col):
      if (col == "Sr. No"):
          return self.check_sno(sno)
      if (col == "Batch"):
          return self.check_batch(sno, value)
      elif ((col == "First Name") or (col == "Last Name")):
          return self.check_firstName(sno, value)
      elif (col == "Email"):
          return self.check_email(sno, value)
      elif (col == "Contact"):
          return self.check_contact(sno, value)



  def check_empty(self,x):
      if ((str(x) == "") or (pd.isna(x)) or (x is None)):
          return "Empty"
      else:
          return "Full"



  def check_sno(self,sno):

      if (self.check_empty(sno) == "Empty"):
          return ["Empty", sno, sno]

      try:
          check = float(sno).is_integer()
      except:
          check = False

      if check:
          return [True, sno, sno]
      else:
          return ["Wrong", sno, sno]



  def romanValid(self,s):
      roman_list = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX',
                    'X', 'XI', 'XII']
      if (s in roman_list):
          return True
      else:
          return False



  def check_batch(self,sno, batch):
      if (self.check_empty(batch) == "Empty"):
          return ["Empty", sno, batch]

      check1 = False
      check2 = False
      batch_part = batch.split("-")
      if (len(batch_part) != 2):
          pass
      else:
          roman = batch_part[0]
          try:
              check1 = self.romanValid(roman)
          except:
              check1 = False

          if (check1):
              section = batch_part[1]

              section_check = re.match("^\s[A-Z]$", section)

              if (section_check is not None):
                  check2 = True

      if (check2):
          return [True, sno, batch]
      else:
          return ["Wrong", sno, batch]



  def check_firstName(self,sno, firstName):
      if (self.check_empty(firstName) == "Empty"):
          return ["Empty", sno, firstName]

      if firstName.replace(" ", "").isalpha():
          return [True, sno, firstName]
      else:
          return ["Wrong", sno, firstName]



  def check_email(self,sno, email):
      if (self.check_empty(email) == "Empty"):
          return ["Empty", sno, email]

      regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

      if (re.search(regex, email)):
          return [True, sno, email]

      else:
          return ["Wrong", sno, email]



  def check_contact(self,sno, contact):

      if (self.check_empty(contact) == "Empty"):
          return ["Empty", sno, contact]

      # 1) Begins with 7 or 8 or 9.
      # 2) Then contains 9 digits
      regex = '^[7-9][0-9]{9}$'
      check = re.search(regex, str(contact))

      if (check):
          return [True, sno, contact]
      else:
          return ["Wrong", sno, contact]


  def format_rule(self,col):
      if (col=="Sr. No"):
          rule="All Sr No should be Integer"
      elif(col=="Batch"):
          rule="Batch should start with a Roman numeral(1-12) immediately followed by a hypen and then there should be a space followed by Section name in Capital letter. For eg IX- C is in correct format"
      elif(col=="First Name"):
          rule="First Name can only contain letter and space. No number or other character is acceptable"
      elif(col=="Last Name"):
          rule="First Name can only contain letter and space. No number or other character is acceptable"
      elif(col=="Email"):
          rule="Email should be of a proper format"

      elif(col=="Contact"):
          rule="10 digit number which starts with 7,8 or 9"

      else:
          rule=""

      return rule





