const container = document.querySelector('.card-list');
const counterId = document.querySelector('#counter');
const api = new Api('http://127.0.0.1:8000/subscriptions/');
const header = new Header(counterId);
const configButton = {
    subscribe: {
        attr: 'data-out',
        default: {
            class: 'button_style_blue',
            text: 'Отписаться'
        },
        active: {
            class: 'button_style_light-blue-outline',
            text: `Подписаться на автора`
        }
    }
}
const subscribe = new Subscribe(configButton.subscribe, api);
const myFollow = new MyFollow(container, '.card-user', header, api, true,{
    subscribe
})
myFollow.addEvent();

