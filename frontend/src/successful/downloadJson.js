import download from "./downloadFunc";

const donwloadJson = (json, filename) => {
  const reportString = JSON.stringify(json);
  const blob = new Blob([reportString], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  download(url, filename);
  URL.revokeObjectURL(url);
};

export default donwloadJson;
