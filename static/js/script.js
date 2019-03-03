$(document).ready(function () {
    console.log("jQuery ready!");
});
var app = new Vue({
    el: '#fast_search_app',
    delimiters: ['[[', ']]'],
    data: {
        message: 'введите что-нибудь',
        search_job: '',
        query_list: [],
    },
    watch: {
        search_job: function () {
            if (this.search_job.length > 2) {
                this.message = 'начинаем поиск';
                if ($('#dropdown_search').is(":hidden")) {
                    $('#dropdown_search').show();
                    this.getVacancies();
                }
            } else {
                this.message = "введите еще что-нибудь"
                $('#dropdown_search').hide();
                this.query_list = [];
            }
        }
    },
    methods: {
        getVacancies: function () {
            this.loading = true;
            this.$http.get('/api/vacancies/')
                .then( response => {
                    response.body.forEach(element => {
                    if (element.title.toLowerCase().includes(this.search_job.toLowerCase())) {
                        this.query_list.push(element.title.toLowerCase());
                        }
                    });
                }).catch(err => {
                    this.loading = false;
                    console.log(err);
                })
        },
        updateQuery(value) {
            this.search_job=value;
        }
    }
})
//updating list item component
Vue.component('v-list-item', {
    props: ['title'],
    template: `
    <button class="dropdown-item" type="button">[[ title ]]</button>
    `
})