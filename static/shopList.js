const container = document.querySelector('.shopping-list');
const counterId = document.querySelector('#counter');
const api = new Api('http://127.0.0.1:8000/shopping_list');
const header = new Header(counterId);

const shopList = new ShopList(container, header, api);
shopList.addEvent();
