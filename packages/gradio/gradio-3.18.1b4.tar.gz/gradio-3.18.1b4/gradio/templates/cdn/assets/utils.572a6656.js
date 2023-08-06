function s(a,e,n){if(a==null)return null;if(typeof a=="string")return{name:"file_data",data:a};if(Array.isArray(a))for(const r of a)s(r,e,n);else a.is_file&&(n==null?a.data=e+"file="+a.name:a.data="proxy="+n+"file="+a.name);return a}export{s as n};
//# sourceMappingURL=utils.572a6656.js.map
