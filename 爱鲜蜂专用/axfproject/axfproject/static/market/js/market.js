$(document).ready(function () {
    var alltypebtn = document.getElementById("alltypebtn")
    var showsortbtn = document.getElementById("showsortbtn")

    var typediv = document.getElementById("typediv")
    var sortdiv = document.getElementById("sortdiv")

    typediv.style.display = "none"
    sortdiv.style.display = "none"



    alltypebtn.addEventListener("click",function () {
        typediv.style.display = "block"
        sortdiv.style.display = "none"

    },false)

     showsortbtn.addEventListener("click",function () {
        typediv.style.display = "none"
        sortdiv.style.display = "block"

    },false)

    typediv.addEventListener("click",function () {
        typediv.style.display = "none"


    },false)

    sortdiv.addEventListener("click",function () {
        sortdiv.style.display = "none"

    },false)


    //修改购物车表
    var addShopings = document.getElementsByClassName("addShoping")
    var subShopings = document.getElementsByClassName("subShoping")

    for (var i = 0; i < addShopings.length; i ++){
        addShoping = addShopings[i]
        
        addShoping.addEventListener("click",function () {
            pid = this.getAttribute('ga')
            $.post('/changecart/0/', {'productid':pid}, function (data) {
                if (data.status == 'success'){
                    document.getElementsById(pid).innerHTML = data.data
                }else {
                    if (data.data == -1) {
                        window.location.href = 'http://127.0.0.1:8000/login/'
                    }//此处写死了 不应写死
                }
            })
        })
    }

    for (var i = 0; i < subShopings.length; i ++) {
        subShoping = subShopings[i]

        subShoping.addEventListener("click", function () {
            pid = this.getAttribute('ga')
            $.post('/changecart/1/', {'productid': pid}, function (data) {
                if (data.status == 'success') {

                }


            })
        })
    }
})