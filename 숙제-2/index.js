console.log('Loading Function');

exports.handler =  async (event, context) => {
    const output = event.records.map((record) => {
        const data = JSON.parse(Buffer.from(record.data, 'base64').toString())
        const date = new Date(data.timestamp)

        const partitionKeys = {
            // partitionKeyFromLambda:
            year: date.getFullYear(),
            month: date.getMonth() + 1,
            day: date.getDate(),
            hour: date.getHours() + 9
        }

        return {
            recordId: record.recordId,
            result: 'Ok',
            data: record.data,
            metadata: {
                partitionKeys
            }
        }
    });
    console.log(`Processing completed. Successful records ${output.length}.`);
    return { records: output };
}