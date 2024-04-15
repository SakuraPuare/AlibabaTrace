import { getDataSchema } from "./schema.js";

export const getHeightWithoutHeader = () => {
  const header = document.querySelector("#header");
  return window.innerHeight - header.clientHeight;
};

export const getColumnDetails = (name) => {
  const schema = getDataSchema(name);
  const ret = [];
  for (let i in schema)
    ret.push({
      key: schema[i][0],
      dataKey: schema[i][0],
      title: schema[i][1],
      width: schema[i][2],
      sortable: true,
    });
  return ret;
};
