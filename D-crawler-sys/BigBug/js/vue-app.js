var app = new Vue({
  el: '#vue-app',
  data: {
    message: 'Hello Vue!',
    newJob: false,
    taskUrls: '',
    taskUrlList: [],
    jobList: [
      {
        id: null,
        job_name: '加载中'
      }
    ],
    jobId: '',
    currentJob: {
      id: '',
      name: '',
      rules: [
      ]
    },
    currentResult: [
    ],
    emptyJob: {
      id: 'NEW',
      name: '',
      rules: [
        //层级0
        {
          selectors:[
            ['',false]
          ],
          reg: ''
        }
      ]
    }
  },
  methods:{
    startJob: function () {
      console.log('start job')
      createTask({
        data: {
          name: this.currentJob.name,
          urls: this.taskUrlList
        },
        success: function (res) {
          alert('任务启动成功！')
        }
      })
    },
    stopJob: function () {
      console.log('stop job')
    },
    addSelector: function (rdx) {
      console.log('add selector', rdx);
      this.currentJob.rules[rdx].selectors.push(['',false]);
    },
    dropSelector: function (rdx, idx) {
      console.log('drop selector', rdx, idx);
      if(confirm('确认删除吗？')) {
        this.currentJob.rules[rdx].selectors.splice(idx,1);
      }
    },
    addLevel: function () {
      this.currentJob.rules.push({
        selectors:[
          ['',false]
        ],
        reg: ''
      })
    },
    dropLevel: function (rdx) {
      if(confirm('确认删除吗？')) {
        this.currentJob.rules.splice(rdx,1);
      }
    },
    createJob: function() {
      createJob({
        name: this.currentJob.name,
        rules: this.currentJob.rules,
      },(res)=>{
        console.log(res)
        window.location.href='./'
      })
    },
    updateJob: function() {
      updateJob({
        name: this.currentJob.name,
        rules: this.currentJob.rules,
      },(res)=>{
        console.log(res)
        window.location.reload()
      })
    },
    deleteJob: function() {
      if (confirm('确认删除吗？')) {
        killJob({
          data:{
            name: this.currentJob.name
          },
          success: function (res) {
            window.location.href="./"
          }
        })
      }
    },
    updateTaskUrls: function(e){
      //console.log(e)
      this.taskUrlList = this.taskUrls.split(/[\s\n]/)
      console.log(this.taskUrlList)
    }
  }
});
$(document).on('ready',function(){
  var res = UrlParam.paramMap();
  var path = getHtmlDocName();
  var result;
  //console.log(path,res);
  if (res.name) {
    console.log('load job');
    console.log('load result');
    app.jobId = res.id[0];
    app.currentJob.name = res.name[0];
    getResult(app.currentJob.name,(result)=>{
      console.log(JSON.parse(result[0].result['rule:rule'][0]))
      //result.splice(0,1);
      app.currentJob = JSON.parse(result[0].result['rule:rule'][0])
      app.currentResult = result;
      setTimeout(()=>{
        // initialization of datatables
        $.HSCore.components.HSDatatables.init('.js-datatable');
        document.querySelectorAll('code').forEach(function (block) {
          hljs.highlightBlock(block)
        })
      },500);
    });
  } else if (path === 'job') {
    console.log('new job');
    app.currentJob = app.emptyJob;
    app.newJob = true;
  } else {
    console.log('job list')
    getJobList((data)=>{
      console.log(data)
      app.jobList = data;
    })
  }
});