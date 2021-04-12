from django.shortcuts import render
from django.http import HttpResponse
from django.template import context, loader
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.



from .models import Cart
from .forms import HistoryForm

from django.conf import settings
import stripe



class TopView(View):
    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.user.id)

        return render(request, 'mysite/top.html')


top = TopView.as_view()



"""
■ 決済処理の大まかな流れ

1、属性に公開鍵をセットしたStripeのJSが発動(ここでstripe側が公開鍵の有効性を確認している)
2、カード番号を入力してカードの有効確認。stripeTokenにセットされDjangoにPOST文が送られる
3、下記のCheckoutViewのPOSTメソッドの処理が実行される。
4、公開鍵に対応した秘密鍵とトークンをセット。(自サイトの公開鍵を使用して決済を試みている事をチェックする)
5、stripe.Charge.createが実行。決済処理が実行される。

"""


class CartView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        print(request.user.id)

        carts   = Cart.objects.filter(user=request.user.id)

        fee     = 0

        for cart in carts:
            fee += cart.product.price * cart.amount

        context = { "carts":carts,
                    
                    'data_key': settings.STRIPE_PUBLISHABLE_KEY,
                    'data_amount': fee, 
                    'data_name':  "通販サイトA",
                    'data_description': "通販サイトAのカート内商品の購入処理",
                    'data_currency': 'JPY',
                }


        return render(request, 'mysite/cart.html', context)

cart    = CartView.as_view()
   


class CheckoutView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):


        stripe.api_key  = settings.STRIPE_SECRET_KEY
        token           = request.POST['stripeToken']

        carts   = Cart.objects.filter(user=request.user.id)
        fee     = 0

        for cart in carts:
            fee += cart.product.price * cart.amount


        #決済処理
        try:
            #トークンを元に決済を実行する
            charge  = stripe.Charge.create(
                    amount= fee,
                    currency='JPY',
                    source=token,
                    description='テスト決済完了',
                    )
            context = { "charge":charge }
    


            #カート内の商品を購入履歴に記録。
            #TIPS:外部キーで関連付けられた主キーを記録する場合、forms.pyもしくはserializer.pyを経由してバリデーションしなければ、DBに記録できない
            for cart in carts:
                data    = { "product" : cart.product.id ,
                            "amount" : cart.amount ,
                            "user" : cart.user.id ,
                        }
                formset = HistoryForm(data)

                if formset.is_valid():
                    print("バリデーションOK")
                    formset.save()
                else:
                    print("バリデーションNG")

            #TODO:実践ではカート内のデータを全て消す。

        except stripe.error.CardError as e:

            #決済が失敗した場合の処理
            context = { "message":"決済に失敗しました" }
            return render(request, 'mysite/error.html', context)

        return render(request, 'mysite/complete.html', context)

checkout    = CheckoutView.as_view()



