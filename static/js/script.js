$(document).ready(function () {
    console.log("jQuery ready!");
});
var app = new Vue({
    el: '#fast_search_app',
    delimiters: ['[[', ']]'],
    data: {
        message: 'введите что-нибудь',
        search_job: '',
        search_city: '',
        query_list: [],
        isActive: false,
        id_dropdown: '',
    },
    watch: {
        search_job: function () {
                if (this.search_job.length > 2) {
                console.log('more');
                this.message = 'начинаем поиск позиций';
                    this.id_dropdown = 'id_position_dropdown';
                    this.isActive = true;
                    this.getVacancies();
            } else {
                this.message = "введите еще что-нибудь";
                this.isActive = false;
                this.query_list = [];
            }
        },
        search_city: function() {
            if (this.search_city.length > 2) {
                this.id_dropdown = 'id_city_dropdown';
                this.message = 'начинаем поиск городов';
                if($('#id_city_dropdown').is(":hidden")) {
                    $("#id_city_dropdown").show();
                    this.getCities();
                } else {
                    this.message = "введите еще что-нибудь";
                    this.query_list = [];
                }
            }
        }
    },
    methods: {
        getQueryType: function(element) {
            console.log($(element).siblings());
        },
        getVacancies: function () {
            this.loading = true;
            this.$http.get('/api/vacancies/')
                .then( response => {
                    response.body.forEach(element => {
                    if (element.title.toLowerCase().includes(this.search_job.toLowerCase())) {
                        this.query_list.push(element.title.toLowerCase());
                        }
                    this.loading=false;
                    });
                }).catch(err => {
                    this.loading = false;
                    console.log(err);
                })
        },
        updateQuery($e) {
            let input_value = $e.target.textContent;
            this.search_job = input_value;
            this.query_list = [];
        }
    }
})
//updating list item component
Vue.component('dropdown-loader', {
    props: {
        id: String,
        isActive: Boolean
    },
    template: `
    <div :id="id" class="dropdown-menu" v-bind:class="{ show: isActive }">
    <button v-if="query_list.length==0" class="dropdown-item" type="button">совпадений нет</button>
    <button v-for="title in query_list" @click="updateQuery($event)" class="dropdown-item" type="button">[[title]]</button>
  </div>
    `
})