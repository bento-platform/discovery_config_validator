import { useState } from 'react';
import { Alert, Divider, Space, Upload, type UploadFile } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import JsonView from 'react18-json-view';

type ReducedErrorDetails = {
  loc?: (string | number)[];
  msg: string;
};

type ValidationResponse = {
  errors: ReducedErrorDetails[];
  warnings: ReducedErrorDetails[];
  config: object | null;
  ok: boolean;
};

const fmtRED = (val: ReducedErrorDetails) => (val.loc ? val.loc.map((li) => li.toString()).join('.') : 'unknown');

const Validator = () => {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [response, setResponse] = useState<ValidationResponse | null>(null);
  return (
    <>
      <Upload.Dragger
        style={{ maxWidth: 400 }}
        accept=".json,application/json"
        action="/api/v1/validate"
        fileList={fileList}
        beforeUpload={(file) => {
          setFileList([file]);
        }}
        onChange={(event) => {
          if (event.file && event.file.status === 'done' && event.file.response) {
            setResponse(event.file.response);
          }
        }}
      >
        <p className="ant-upload-drag-icon">
          <UploadOutlined />
        </p>
        <p className="ant-upload-text">
          Click or drag discovery configuration JSON to this area to upload and validate
        </p>
      </Upload.Dragger>
      {response && (
        <>
          <Divider />
          <Space direction="vertical" style={{ width: '100%' }}>
            <Alert
              type={response.ok ? 'success' : 'error'}
              message={`File is${response.ok ? '' : ' not'} a valid discovery configuration`}
            />
            {response.errors.map((err, ei) => (
              <Alert key={ei} type="error" message={`Error at ${fmtRED(err)}`} description={err.msg} />
            ))}
            {response.warnings.map((warn, wi) => (
              <Alert key={wi} type="warning" message={`Warning at ${fmtRED(warn)}`} description={warn.msg} />
            ))}
            {response.config && <JsonView src={response.config} enableClipboard={false} collapsed={2} />}
          </Space>
        </>
      )}
    </>
  );
};

export default Validator;
