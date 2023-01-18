function filterp(val,nameid,key){
    let select = document.getElementById(nameid);
    select.innerHTML='';
    opt = document.createElement('option');
    opt.innerHTML = "..select..";
    select.appendChild(opt);
    if (key=="product"){
        {{ datalav.portpolio|safe }}.forEach(item => {

                if (val==item.product){
                    opt = document.createElement('option');
                    opt.value = item.portfolio_name;
                    opt.innerHTML = item.portfolio_name;
                    select.appendChild(opt);


                }
            })
        }
    if (key=="op_rights"){
        {{ datalav.portpolio|safe }}.forEach(item => {

                if (val==item.operations_right){
                    opt = document.createElement('option');
                    opt.value = item.portfolio_name;
                    opt.innerHTML = item.portfolio_name;
                    select.appendChild(opt);


                }
            })
        }
    if (key=="role"){
        {{ datalav.portpolio|safe }}.forEach(item => {
                if (val==item.role){
                    opt = document.createElement('option');
                    opt.value = item.portfolio_name;
                    opt.innerHTML = item.portfolio_name;
                    select.appendChild(opt);


                }
            })
        }
    if (key=="data_type"){
        {{ datalav.portpolio|safe }}.forEach(item => {
                if (val==item.data_type){
                    opt = document.createElement('option');
                    opt.value = item.portfolio_name;
                    opt.innerHTML = item.portfolio_name;
                    select.appendChild(opt);


                }
            })
        }
        if (key=="member"){
        {{ datalav.portpolio|safe }}.forEach(item => {
                if (val==item.username){
                    opt = document.createElement('option');
                    opt.value = item.portfolio_name;
                    opt.innerHTML = item.portfolio_name;
                    select.appendChild(opt);


                }
            })
        }
}
function filterlevel(myval,nameid1,level){
    let input = document.getElementById(nameid1);
    input.innerHTML='';
    select.appendChild(opt);
    if (level=="level1"){
        {{ datalav.organisations.0.level1.items|safe }}.forEach(item => {

                if (myval==item.item_name){
                    input.innerHTML = item;


                }
            })
        }

}