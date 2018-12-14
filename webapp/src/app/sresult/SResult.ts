export class SResult {
  _index: String;
  _type: String;
  _id: String;
  _score: number;
  _source: {
    annotation: String;
    author: String;
    title: String;
    year: number;
    genre: String;
    id: number;
  };
}
