window.addEvent('domready',function() {

    //You may will need to change category, id_subcategory, and id_selected_cat
    //to match the names of the fields that you are working with.
    var category = $('category');
    var subcategory = $('id_subcategory');

    var update_subcat = function() {
        var cat_id = $('id_selected_cat').value;
        if (cat_id) {
            $('id_selected_cat').value='';
            category.value=cat_id;
        } else {
            cat_id = category.getSelected()[0].value;
        }
        //cat_id = category.getSelected()[0].value;
        var subcat_id = subcategory.getSelected()[0].value;
        var request = new Request.JSON({
            url: "/product/subcategory/"+cat_id+"/",
            onComplete: function(subcats){
                subcategory.empty();
                if (subcats) {
                    subcats.each(function(subcat) {
                        var o = new Element('option', {
                            'value':subcat.pk,
                            'html':subcat.fields.name
                        });
                        if (subcat.pk == subcat_id) {
                            o.set('selected','selected');
                        }
                        o.inject(subcategory);
                    });
                } else {
                    var o = new Element('option', {
                        'value':'',
                        'html':'Please Choose A Category First'
                    });
                    o.inject(subcategory);
                }
            }
        }).get();
    };
    update_subcat();

    category.addEvent('change', function(e){
        e.stop();
        update_subcat();
    });

});



// $(function () {
// // inspect html to check id of category select dropdown.
// $(document).on("change", "select#id_categorys", function () {
// $.getJSON("shop/subcategory/", { id: $(this).val() }, function (j) {
// var options = '<option value="">---------</option>';
// for (var i = 0; i < j.length; i++) {
// options +=
// '<option value="' + j[i].id + '">' + j[i].name + "</option>";
// }
// // inspect html to check id of subcategory select dropdown.
// $("select#id_subcategory").html(options);
// });
// });
// });








// $(function(){
//     // inspect html to check id of category select dropdown.
//     $(document).on('change', "select#id_category_id", function(){
//         $.getJSON("/getSubcategory/",{id: $(this).val()}, function(j){
//              var options = '<option value="">---------</option>';
//              for (var i = 0; i < j.length; i++) {
//                  options += '<option value="' + j[i].id + '">' + j[i].name + '</option>';
//              }
//              // inspect html to check id of subcategory select dropdown.
//              $("select#id_subcategory_id").html(options);
//          });
//      });
//  });