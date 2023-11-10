const selectedModules = JSON.parse(document.getElementById('selected_modules').textContent);
const selectedTargets = JSON.parse(document.getElementById('selected_targets').textContent);
const selectedLanguage = JSON.parse(document.getElementById('selected_languages').textContent);
const optionsTargets = JSON.parse(document.getElementById('course_targets_dict').textContent);
const optionsModules = JSON.parse(document.getElementById('modules_dict').textContent);
const optionsLanguage = JSON.parse(document.getElementById('languages_dict').textContent);


Vue.component('select-2', {
    template: '<select v-bind:name="name" class="form-control" v-bind:multiple="multiple"></select>',
    props: {
      name: '',
      options: {
        Object
      },
      value: null,
      multiple: {
        Boolean,
        default: false

      }
    },
    data() {
      return {
        select2data: []
      }
    },
    mounted() {
      this.formatOptions()
      let vm = this
      let select = $(this.$el)
      select
        .select2({
        placeholder: 'Выберете из списка',
        theme: 'bootstrap',
        width: '100%',
        allowClear: true,
        data: this.select2data
      })
        .on('change', function () {
        vm.$emit('input', select.val())
      })
      select.val(this.value).trigger('change')
    },
    methods: {
      formatOptions() {
        this.select2data.push({ id: '', text: 'Select' })
        for (let key in this.options) {
          this.select2data.push({ id: key, text: this.options[key] })
        }
      }
    },
    destroyed: function () {
      $(this.$el).off().select2('destroy')
    }
  })

const multiSelectModules = Vue.component('multiple-select-modules', {
    data() {
        return {
            selected: selectedModules,
            optionsModules
        }
    }
})

  const multiSelectLanguage = Vue.component('multiple-select-language', {
    data () {
      return {
        selected: selectedLanguage,
        optionsLanguage
      }
    }
  })

  const multiSelectCA = Vue.component('multiple-select-targets', {
    data () {
      return {
        selected: selectedTargets,
        optionsTargets
      }
    }
  })

  const modules = new Vue({
    el: '#modules',
  })

  const ca = new Vue({
    el: '#targets',
  })

  const language = new Vue({
    el: '#languages',
  })

