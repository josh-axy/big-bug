UrlParam = function() { // url参数
  var data, index;
  (function init() {
    data = []; //值，如[["1","2"],["zhangsan"],["lisi"]]
    index = {}; //键:索引，如{a:0,b:1,c:2}
    var u = window.location.search.substr(1);
    if (u !== '') {
      var params = decodeURIComponent(u).split('&');
      for (var i = 0, len = params.length; i < len; i++) {
        if (params[i] !== '') {
          var p = params[i].split("=");
          if (p.length === 1 || (p.length === 2 && p[1] === '')) {// p | p= | =
            data.push(['']);
            index[p[0]] = data.length - 1;
          } else if (typeof(p[0]) === 'undefined' || p[0] === '') { // =c 舍弃

          } else if (typeof(index[p[0]]) === 'undefined') { // c=aaa
            data.push([p[1]]);
            index[p[0]] = data.length - 1;
          } else {// c=aaa
            data[index[p[0]]].push(p[1]);
          }
        }
      }
    }
  })();
  return {
    // 获得参数,类似request.getParameter()
    param : function(o) { // o: 参数名或者参数次序
      try {
        return (typeof(o) === 'number' ? data[o][0] : data[index[o]][0]);
      } catch (e) {
      }
    },
    //获得参数组, 类似request.getParameterValues()
    paramValues : function(o) { // o: 参数名或者参数次序
      try {
        return (typeof(o) === 'number' ? data[o] : data[index[o]]);
      } catch (e) {}
    },
    //是否含有paramName参数
    hasParam : function(paramName) {
      return typeof(paramName) === 'string' ? typeof(index[paramName]) !== 'undefined' : false;
    },
    // 获得参数Map ,类似request.getParameterMap()
    paramMap : function() {
      var map = {};
      try {
        for (var p in index) { map[p] = data[index[p]]; }
      } catch (e) {}
      return map;
    }
  }
}();
function getHtmlDocName() {
  var str = window.location.href;
  str = str.substring(str.lastIndexOf("/") + 1);
  str = str.substring(0, str.lastIndexOf("."));
  return str;
}
function getResult(name,success) {
  $.ajax({
    type: 'POST',
    url: 'http://localhost:8888/getResult',
    //contentType: 'application/json',
    data: {
      job_name: name
    },
    success: function(data) {
      if (data.success){
        var result = JSON.parse(data.data)
        //console.log(result[1].result['results:0'][0])
        success(result)
      }
    }
  })
}

function getJobList(success) {
  $.ajax({
    url: 'http://localhost:8888/jobList',
    //contentType: 'application/json',
    success: function(data) {
      if (data.success){
        var result = JSON.parse(data.data)
        //console.log(result[1].result['results:0'][0])
        success(result)
      }
    }
  })
}

function createJob(data,success) {
  $.ajax({
    url: 'http://localhost:8888/createJob',
    type: 'POST',
    data: {
      job_name: data.name,
      rules: JSON.stringify(data.rules)
    },
    //contentType: 'application/json',
    success: function(res) {
      if (res.success){
        alert('创建成功！')
        //console.log(result[1].result['results:0'][0])
        success(res)
      } else {
        alert('创建失败！请重试')
      }
    }
  })
}

function updateJob(data,success) {
  $.ajax({
    url: 'http://localhost:8888/updateJob',
    type: 'POST',
    data: {
      job_name: data.name,
      rules: JSON.stringify(data.rules)
    },
    //contentType: 'application/json',
    success: function(res) {
      if (res.success){
        alert('保存成功！')
        //console.log(result[1].result['results:0'][0])
        success(res)
      } else {
        alert('保存失败！请重试')
      }
    }
  })
}

function createTask({data,success}) {
  $.ajax({
    url: 'http://localhost:8888/createTask',
    type: 'POST',
    data: {
      job_name: data.name,
      urls: JSON.stringify(data.urls)
    },
    //contentType: 'application/json',
    success: function(res) {
      if (res.success){
        success(res)
      }
    }
  })
}

function pauseJob({data,success}) {
  $.ajax(({
    url: 'http://localhost:8888/createTask',
    type: 'POST',
    data: {
      job_name: data.name
    },
    success: function (res) {
      if (res.success) {
        success(res)
      }
    }
  }))
}

function killJob({data,success}) {
  $.ajax(({
    url: 'http://localhost:8888/killCrawler',
    type: 'POST',
    data: {
      job_name: data.name
    },
    success: function (res) {
      if (res.success) {
        alert('删除成功！')
        success(res)
      }
    }
  }))
}