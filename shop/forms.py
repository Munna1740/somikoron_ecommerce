from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput

class SignUpForm(forms.Form):
    class Meta:
        model = User
    Phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'label': 'Mobile'}))
    Password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'Label':
                                                                                      'Password'}))

    labels = {
        'username': 'Phone',
        'password1': 'Password'
    }

    help_texts = {
        'username': None,
        'password1': None,
    }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        password2 = None
        username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'label': 'Mobile'}))
        fields = ['username', 'password1']
        password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'id': ''}))

        labels = {
            'username': 'Phone'
        }
        widgets = {
            'password1': PasswordInput()
        }
        help_texts = {
            'username': None,
            'password': None,
        }


PAYMENT_CHOICES = (
    ('CASH ON', 'Cash on Delivery'),
    # ('Bkash', 'bKash Payment'),
)
DIVISION_CHOICES = (
    ('Dhaka', 'Dhaka'),
    # ('Barishal', 'Barishal'),
    # ('Khulna', 'Khulna'),
    # ('Sylhet', 'Sylhet'),
    # ('Rajshahi', 'Rajshahi'),
    # ('Rangpur', 'Rangpur'),
    # ('Chattagram', 'Chattagram'),
)
DISTRICT_CHOICES = (
    ('Dhaka', 'Dhaka'),
    # ('Barishal', 'Barishal'),
    # ('Khulna', 'Khulna'),
    # ('Sylhet', 'Sylhet'),
    # ('Rajshahi', 'Rajshahi'),
    # ('Rangpur', 'Rangpur'),
    # ('Chattagram', 'Chattagram'),
)
AREA_CHOICES = (
    ('Dhanmondi', 'Dhanmondi'),
    ('Mohammadpur', 'Mohammadpur'),
    ('Adabor', 'Adabor'),
    ('Mirpur', 'Mirpur'),
    ('Shyamoli', 'Shyamoli'),
    ('Kallyanpur', 'Kallyanpur'),
    ('Azimpur', 'Azimpur'),
    ('Agargaon', 'Agargaon'),
    ('Banani', 'Banani'),
    ('Gulshan', 'Gulshan'),
    ('Magbazar', 'Magbazar'),
    ('Rampura', 'Rampura'),
    ('Mohakhali', 'Mohakhali'),
)


class CheckoutForm(forms.Form):
    address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2,
                                                                          'cols': 70,
                                                                          'id':'address'}))
    address.widget.attrs.update({'placeholder': ''})
    customer_phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'phone', }))
    customer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'id': 'customer_name', })
    )
    area = forms.CharField(
        widget=forms.Select(choices=AREA_CHOICES, attrs={'style': 'height:62px', 'id':'area'}),
        required=True

    )
    order_notes = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'rows': 3, 'cols': 85}),
                                  max_length=160)
    payment_option = forms.ChoiceField(required=True,
                                           widget=forms.RadioSelect, initial='CASH ON', choices=PAYMENT_CHOICES)
    labels = {
        'customer_name' : 'Name',
        'customer_phone': 'Phone',
    }


    # ('ADA', 'Adabor'),
    # ('AFT', 'Aftabnagar'),
    # ('AGR', 'Agargaon'),
    # ('AMD', 'Ahmednagar'),
    # ('ALB', 'Alu Bazar'),
    # ('AMB', 'Amin Bazar'),
    # ('ACP', 'Ansar Camp'),
    # ('ARB', 'Arambug'),
    # ('ART', 'Armanitola'),
    # ('ASK', 'Ashkona'),
    # ('ASL', 'Ashulia'),
    # ('AZM', 'Azimpur'),
    # ('AZP', 'Azampur'),
    # ('BBA', 'Babubazar'),
    # ('BDA', 'Badda'),
    # ('BLR', 'Bailey Road'),
    # ('BKB', 'Bakshibazar'),
    # ('BAN', 'Banani'),
    # ('BNS', 'Banashree'),
    # ('BNM', 'Bangla motor'),
    # ('BAS', 'Bangshal'),
    # ('BRD', 'Baridhara'),
    # ('BSB', 'Basabo'),
    # ('BSD' 'Bashundhara'),
    # ('BSL', 'Bosila'),
    # ('CHD', 'Chad Uddan'),
    # ('CHN', 'Chankharpul'),
    # ('CTR', 'Chittagong Road'),
    # ('DRS', 'Darussalam'),
    # ('DMR', 'Demra'),
    # ('DHC', 'Dhaka Cantonment'),
    # ('DHN', 'Dhanmondi'),
    # ('DHO', 'Dhonia'),
    # ('DHP', 'Dhupkhola'),
    # ('DKK', 'Dokkhin Khan'),
    # ('DYG', 'Doyagonj'),
    # ('ECB', 'ECB Chattar'),
    # ('EPR', 'Elephant Road'),
    # ('ESK', 'Eskaton'),
    # ('FRG', 'Farmgate'),
    # ('FYD', 'Faydabad'),
    # ('FKR', 'Fokirapul'),
    # ('GAB', 'Gabtoli'),
    # ('GND', 'Gandaria'),
    # ('GLP', 'Golapbag'),
    # ('GPB', 'Gopibag'),
    # ('GOR', 'Goran'),
    # ('GRR', 'Green Road'),
    # ('GUL', 'Gulisthan'),
    # ('GLS', 'Gulshan'),
    # ('HAB', 'Hazaribagh'),
    # ('HTJ', 'Hatirjheel'),
    # ('HTP', 'Hatirpool'),
    # ('HMP', 'Hemayetpur'),
    # ('IBR', 'Ibrahimpur'),
    # ('IND', 'Indira Road'),
    # ('ISL', 'Islambagh'),
    # ('ISP', 'Islampur'),
    # ('JFR', 'Jafrabad'),
    # ('JTR', 'Jatrabari'),
    # ('JGT', 'Jigatola'),
    # ('JUR', 'Jurain'),
    # ('KFR', 'Kafrul'),
    # ('KLP', 'Kallyanpur'),
    # ('KLS', 'Kalshi'),
    # ('KTB', 'Katabon'),
    # ('KTG', 'Kathalbagan'),
    # ('KWR', 'Kawran Bazar'),
    # ('KZP', 'Kazipara'),
    # ('KHL', 'Khilgaon'),
    # ('KLK', 'Khilkhet'),
    # ('KCK', 'Kochukhet'),
    # ('KLB', 'Kolabagan'),
    # ('KMP', 'Komlapur'),
    # ('KUR', 'Kuril'),
    # ('LKB', 'Lakshmi Bazar'),
    # ('LLB', 'Lalbagh'),
    # ('LLM', 'Lalmatia'),
    # ('MLB', 'Malibagh'),
    # ('MLT', 'Malitola'),
    # ('MNG', 'Manik Nagar'),
    # ('MIR', 'Mirpur'),
    # ('MDB', 'Modhubag'),
    # ('MOG', 'Mogbazar'),
    # ('MOH', 'Mohakhali'),
    # ('MMD', 'Mohammadpur'),
    # ('MNP', 'Monipur'),
    # ('MPP', 'Monipuri para'),
    # ('MTJ', 'Motijheel'),
    # ('MUC', 'Mouchak'),
    # ('NKH', 'Nakhalpara'),
    # ('NAR', 'Narinda'),
    # ('NYP', 'Noya paltan'),
    # ('NEW', 'Newmarket'),
    # ('NIK', 'Niketon'),
    # ('NKG', 'Nikunjo'),
    # ('PKP', 'Paikpara'),
    # ('PLB', 'Pallabi'),
    # ('PLT', 'Paltan'),
    # ('PNT', 'Panthapath'),
    # ('PRB', 'Paribagh'),
    # ('PTT', 'Patuatuli'),
    # ('PIR', 'Pirerbagh'),
    # ('PST', 'Postakhola'),
    # ('PRP', 'Puran Paltan'),
    # ('PRD', 'Puran Dhaka'),
    # ('PUR', 'Purobi'),
    # ('RJB', 'Rajabazar'),
    # ('RAJ', 'Rajarbagh'),
    # ('RAM', 'Ramna'),
    # ('RMP', 'Rampura'),
    # ('RAY', 'Rayerbagh'),
    # ('RYB', 'Rayerbazar'),
    # ('SAN', 'Sangkar'),
    # ('SAV', 'Savar'),
    # ('SYD', 'Sayedabad'),
    # ('SEG', 'Segunbagicha'),
    # ('SHB', 'Shahbag'),
    # ('SHA', 'Shahjadpur'),
    # ('SHJ', 'Shajahanpur'),
    # ('SHM', 'Shyamoli'),
    # ('SHN', 'Shantinagar'),
    # ('SHK', 'Shekhertek'),
    # ('SHW', 'Shewra'),
    # ('SWP', 'Shewrapara'),
    # ('SDD', 'Siddheswari'),
    # ('SNK', 'Sonir Akhra'),
    # ('SUK', 'Shukrabad'),
    # ('SUT', 'Sutrapur'),
    # ('TAT', 'Taltola'),
    # ('TEJ', 'Tejgaon'),
    # ('TJP', 'Tejkunipara'),
    # ('TKT', 'Tikatoli'),
    # ('TKK', 'Tikkapara'),
    # ('TLB', 'Tolarbag'),
    # ('TLD', 'Tollabad'),
    # ('TOP', 'Topkhana Road'),
    # ('UTT', 'Uttara'),
    # ('WAR', 'Wari'),
