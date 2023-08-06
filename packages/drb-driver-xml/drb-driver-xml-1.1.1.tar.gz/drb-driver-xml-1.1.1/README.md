# XmlNode Implementation
This drb-driver-xml module implements xml format access with DRB data model. It
is able to navigates among the xml contents.

## Xml Factory and Xml Node
The module implements the basic factory model defined in DRB in its node
resolver. Based on the python entry point mechanism, this module can be
dynamically imported into applications.

The entry point group reference is `drb.driver`.<br/>
The driver name is `xml`.<br/>
The factory class `XmlNodeFactory` is encoded into `drb.drivers.factory`
module.<br/>

The xml factory creates a XmlNode from an existing xml content. It uses a base
node to access the content data using the streamed base node implementation.

The base node can be a FileNode (See drb-driver-file), HttpNode, ZipNode or any
other node able to provide streamed (`BufferedIOBase`, `RawIOBase`, `IO`) xml
content.

## limitations
The current version does not manage child modification and insertion. XmlNode
is currently read only.

## Using this module
To include this module into your project, the `drb-driver-xml` module shall be
referenced into `requirement.txt` file, or the following pip line can be run:
```commandline
pip install drb-driver-xml
```
