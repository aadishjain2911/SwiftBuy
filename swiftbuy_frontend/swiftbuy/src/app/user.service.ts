import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';
import { Registration_info } from './registration_details';
import {Cart} from './cart';

@Injectable({ providedIn: 'root' })
export class UserService {
    constructor(private http: HttpClient, private cookieService: CookieService) { }

    getNotifications(): Observable<any> {
        console.log('getNotifications');
        return this.http.get(`http://localhost:8000/notifications`, { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });
    }

    getProduct(productid: number): Observable<any> {
        console.log('getProduct productid: ' + productid);
        return this.http.get('http://localhost:8000/catalog/products/'+String(productid), { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true} );

    }

    getCatalogProducts(categoryid: number): Observable<any> {
        console.log('getCatalogProducts');
        return this.http.get('http://localhost:8000/catalog/' + String(categoryid), { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true});
    }    
        
    addMoney(money: any): Observable<any>{
        console.log(money)
        return this.http.post(`http://localhost:8000/addmoney`, money, { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });
    }

    getCart(): Observable<any> {
        console.log('getCart');
        return this.http.get(`http://localhost:8000/cart`, { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });
    }

    placeOrder(paymentid: number): Observable<any> {
        return this.http.post(`http://localhost:8000/order/`, {"payment_id":paymentid}, { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });
    }

    // register(user: User) {
    //     console.log('register user: ' + JSON.stringify(user));
    //     return this.http.post('http://192.168.0.104:8000/signup/', (user));
    // }

    // login(user: Login) {
    //     console.log('Login user: ' + JSON.stringify(user));
    //     return this.http.post('http://192.168.0.104:8000/login/', (user));
    // }

    // delete(id: number) {
    //     return this.http.delete(`${config.apiUrl}/users/${id}`);
    // }

    getProfile(): Observable<any>{
        return this.http.get(`http://localhost:8000/about/`, { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });
    }

    updateProfile(user:Registration_info) : Observable<any>{
        console.log(user)
        return this.http.post(`http://localhost:8000/about/`, {user}, { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });
    }

    getWalletHistory(){
        return this.http.post(`http://localhost:8000/wallet/`, {},{ headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });        
    }

    // addMoneyToWallet(){
    //     return this.http.post(`http://localhost:8000/about`, { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });
    // }

    getBuyHistory(){
        return this.http.get(`http://localhost:8000/buyinfo/history`, { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true });
    }

    addToCart(cart: Cart): Observable<any>{
        return this.http.post(`http://localhost:8000/cart`, cart,  { headers: { 'Content-Type': 'application/json','X-CSRFToken': this.cookieService.get('csrftoken')  }, withCredentials: true }); 
    }

}