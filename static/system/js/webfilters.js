function FiltersObject()
{

    this.classes = {
        'offSubmit': '.submit-false',
        'onSubmit': '.submit-true',
        'onChecked': [
            'input[type="text"]',
            'select',
            'input[type="checkbox"]',
            'input[type="radio"]'
        ].join()
    };

    this.list_elements = [
        'select',
        'input[type="text"]',
        'input[type="hidden"]',
        'input[type="checkbox"]:checked',
        'input[type="radio"]:checked'
    ];

    this.init = function init()
    {
        if($(this.classes.offSubmit).length === 0)
        {
            return false;
        }
    };

    this.renderForm = function renderForm()
    {
        var values = [];
        var inputs = $(this.classes.offSubmit).find(this.list_elements.join());
        var html = '';

        for (var i=0; i<inputs.length; i++)
        {
            values.push({
                'name': inputs.eq(i).attr('name'),
                'value': inputs.eq(i).val()
            });
            html += '<input type="hidden" name="'+ values[i].name +'" value="'+ values[i].value +'"/>';
        }
        return html;
    };

    this.onSubmit = function onSubmit(elem)
    {
        if($(this.classes.onSubmit).length === 0)
        {
            return true;
        }
        var t = this.renderForm();
        $(this.classes.onSubmit).html(t);
        $(this.classes.onSubmit).submit();
        return false;
    };
}

var FiltersAggregate = new FiltersObject();

if($(FiltersAggregate.classes.offSubmit).length > 0)
{
    $(FiltersAggregate.classes.onChecked).change(function(){
        $(this).closest('form').submit();
    });

    $(FiltersAggregate.classes.offSubmit).submit(function(){
        return FiltersAggregate.onSubmit(this);
    });
}