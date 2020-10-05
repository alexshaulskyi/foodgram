const container = document.querySelector('.single-card');
const counterId = document.querySelector('#counter');
const api = new Api('http://127.0.0.1:8000/detail_recipe/');
const header = new Header(counterId);

const configButton = {
    purchpurachases: {
        attr: 'data-out',
        default: {
            class: 'button_style_blue',
            text: '<span class="icon-plus button__icon"></span>Добавить в покупки'
        },
        active: {
            class: 'button_style_light-blue-outline',
            text: `<span class="icon-check button__icon"></span> Рецепт добавлен`
        }
    }
}
const purchpurachases = new Purchpurachases(configButton.purchpurachases, api);


const singleCard = new SingleCard(container, '.single-card', header, api, false,{
    purchpurachases,
});
singleCard.addEvent();


