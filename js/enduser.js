$(function () {
    var fx = function fx() {
    $(".stat-number").each(function (i, el) {
        var data = parseInt(this.dataset.n, 10);
        var props = {
            "from": {
                "count": 0
            },
                "to": { 
                "count": data
            }
        };
        $(props.from).animate(props.to, {
            duration: 1000 * 1,
            step: function (now, fx) {
                $(el).text(Math.ceil(now));
            },
            complete:function() {
                if (el.dataset.sym !== undefined) {
                  el.textContent = el.textContent.concat(el.dataset.sym)
                }
            }
        });
    });
    };
    
    var reset = function reset() {
        //console.log($(this).scrollTop())
        if ($(this).scrollTop() > 90) {
            $(this).off("scroll");
          fx()
        }
    };
    
    $(window).on("scroll", reset);
});

function toggleEl(cl, id) {
    var current = document.getElementById(id);
    $(cl).css("display", "none");
    current.style.display = "block";
}

function tradCriteria() {
    var text = 
        "• accuracy (syntactic and semantic): the data, and its attributes, correctly represents the true value of the concept or event to which it refers \n" +
        "• consistency: the data, and its attributes, does not present contradictions with other data in the context of use of the owner administration  \n" +
        "• completeness: the data is exhaustive for all its expected values and with respect to the related entities (sources) that contribute to the definition of the process \n" +
        "• timeliness (or timeliness of updating): the data, and its attributes, is of the 'right time' (is up-to-date) with respect to the proceedings to which it refers"
    alert(text)
}