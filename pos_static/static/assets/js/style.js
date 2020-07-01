
// Default initialization
$(".styled, .multiselect-container input").uniform({
    radioClass: 'choice'
});

// File input
$(".file-styled").uniform({
    wrapperClass: 'bg-blue',
    fileButtonHtml: '<i class="icon-file-plus"></i>'
});


//
// Contextual colors
//

// Primary
$(".control-primary").uniform({
    radioClass: 'choice',
    wrapperClass: 'border-primary-600 text-primary-800'
});

// Danger
$(".control-danger").uniform({
    radioClass: 'choice',
    wrapperClass: 'border-danger-600 text-danger-800'
});

// Success
$(".control-success").uniform({
    radioClass: 'choice',
    wrapperClass: 'border-success-600 text-success-800'
});

// Warning
$(".control-warning").uniform({
    radioClass: 'choice',
    wrapperClass: 'border-warning-600 text-warning-800'
});

// Info
$(".control-info").uniform({
    radioClass: 'choice',
    wrapperClass: 'border-info-600 text-info-800'
});

// Custom color
$(".control-custom").uniform({
    radioClass: 'choice',
    wrapperClass: 'border-indigo-600 text-indigo-800'
});

//counts table rows

function count_table_rows(table_class, tbadge_class) {
    let rows = $('.' + table_class + ' tbody').children().length;
    $('.' + tbadge_class + '').html(rows);
}

function print_system_doc(print_doc) {
    var mywindow = window.open('', 'PRINT', 'height=600,width=1000');
    let html_page = `
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Print_Document</title>
    <style>
        html{
            text-transform: uppercase;
            font-family: Arial;
        }
        table{
            font-family: Arial;
        }
    </style>
</head>
<body>
    `+print_doc+`
</body>
</html>
        `;
    mywindow.document.write(html_page);

    mywindow.document.close(); // necessary for IE >= 10
    mywindow.focus(); // necessary for IE >= 10*/

    mywindow.print();
    // mywindow.close();
}