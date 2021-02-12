function renderTable(html_id, data) {
    $("#" + html_id).html('<table id="resultTable"></table>');

    $('#resultTable').bootstrapTable({
        columns: [

        {
            field: 'poster',
            title: 'Poster',
            sortable: true,
            formatter: posterImage
        },
        {
            field: 'name',
            title: 'Name',
            sortable: true
        },
        {
            field: 'year',
            title: 'Year',
            sortable: true
        },
        {
            field: 'description',
            title: 'Description'
        },
        {
            field: 'availability.Netflix',
            title: 'Netflix',
            sortable: true,
            formatter: netflixImage
        },
        {
            field: 'availability.Amazon',
            title: 'Amazon',
            sortable: true,
            formatter: amazonImage
        },
        {
            field: 'availability.Disney+',
            title: 'Disney+',
            sortable: true,
            formatter: disneyImage
        },
        {
            field: 'num_available',
            title: 'N',
            visible: false
        }
        ],
        data: data["result"],
        //sortName: "num_available",
        //sortOrder: "desc"
      })
}

function countFormatter(value) {
    return value.toString();
}

function posterImage(value) {
    return '<img src="' + value + '" alt="" height="200">';
}

function netflixImage(value) {
    return `${value ? '<img src="static/assets/netflix.png" width="30" alt="">' : '<img src="static/assets/netflix.png" width="30" style="opacity:0.1" alt="">'}`
}

function amazonImage(value) {
    return `${value ? '<img src="static/assets/prime.png" width="30" alt="">' : '<img src="static/assets/prime.png" width="30" style="opacity:0.1" alt="">'}`
}

function disneyImage(value) {
    return `${value ? '<img src="static/assets/disney.png" width="30" alt="">' : '<img src="static/assets/disney.png" width="30" style="opacity:0.1" alt="">'}`
}